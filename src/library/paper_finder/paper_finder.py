from library.webscraper.webscraper import Webscraper
from library.search_input.search_input import SearchInput
from library.downloader.downloader import Downloader, DownloadSummary
import string
import re

SCHOLAR_URL = "https://scholar.google.com/scholar?q="

# Patterns for resolving direct PDF links without loading the landing page.
# Checked in order first match wins.
_DIRECT_PDF_PATTERNS = [
    # arXiv abstract page   PDF
    (re.compile(r'arxiv\.org/abs/([\d.]+)'), "https://arxiv.org/pdf/{0}.pdf"),
    # Semantic Scholar     PDF  (common pattern)
    (re.compile(r'semanticscholar\.org/paper/[^/]+/([a-f0-9]+)'), None),  # handled in code
]


class PaperFinder:
    def __init__(self):
        self.webscraper = Webscraper()
        self.downloader = Downloader(max_retries=3, retry_delay=2.0)

    def get_seach_keywords(self, search: SearchInput) -> list:
        clean_query: str = search.query.translate(
            str.maketrans('', '', string.punctuation)
        )
        keywords = clean_query.split(" ")
        return keywords

    def create_url(self, search: SearchInput) -> str:
        target_url: str = SCHOLAR_URL
        keywords = self.get_seach_keywords(search)
        keyword_count: int = len(keywords)
        for index, keyword in enumerate(keywords):
            target_url += keyword
            if keyword_count != index + 1:
                target_url += "+"
        if search.year_start:
            target_url += "&as_ylo=" + str(search.year_start)
        if search.year_end:
            target_url += "&as_yhi=" + str(search.year_end)
        return target_url
    ## DO NOT automate testing this Scholar will detect & block us
    def search(self, search: SearchInput) -> list[dict]:
        search_results: list[dict] = []

        target_url = self.create_url(search)
        status = self.webscraper.load_url(target_url)
        if status != True:
            print("Error pulling page HTML...")
            return search_results
        status = self.webscraper.initialize_soup()
        if status != True:
            print("Error creating soup...")
            return search_results

        soup = self.webscraper.soup
        results = soup.find_all("div", class_="gs_r")

        for result in results:
            # Title + link
            title_tag = result.find("h3", class_="gs_rt")
            if not title_tag:
                continue
            link_tag = title_tag.find("a")
            if not link_tag:
                continue

            # Authors + year live in .gs_a
            authors, year = self._parse_meta(result)

            # PDF link shown directly on the Scholar results page (gs_or_ggsm)
            inline_pdf = self._extract_inline_pdf(result)

            search_results.append({
                "title":    link_tag.get_text(),
                "link":     link_tag.get("href"),
                "year":     year,
                "authors":  authors,
                "pdf_link": inline_pdf,
            })

        # Trim to the requested number of results
        search_results = search_results[: search.num_results]

        return search_results

    def enrich_pdf_links(self, papers: list[dict]) -> list[dict]:
        """
        Attempts to populate "pdf_link" for every paper that doesn't already
        have one.  Works in two passes:

        1. Pattern matching instant, no network request (arXiv etc.)
        2. Landing-page scrape loads the paper's URL and hunts for a PDF link.
           Only done when pass 1 fails, to keep requests minimal.

        Mutates each dict in-place and returns the same list.
        """
        for paper in papers:
            if paper.get("pdf_link"):
                continue

            link = paper.get("link", "")
            if not link:
                continue

            # Pass 1 pattern matching
            resolved = self._resolve_by_pattern(link)
            if resolved:
                paper["pdf_link"] = resolved
                continue

            # Pass 2 scrape landing page
            resolved = self._resolve_by_scraping(link)
            if resolved:
                paper["pdf_link"] = resolved

        return papers

    def _resolve_by_pattern(self, url: str) -> str | None:
        """Return a direct PDF URL using known site patterns, or None."""
        # Already a PDF
        if url.lower().endswith(".pdf"):
            return url

        # arXiv
        m = re.search(r'arxiv\.org/abs/([\d.]+)', url)
        if m:
            return f"https://arxiv.org/pdf/{m.group(1)}.pdf"

        return None

    def _resolve_by_scraping(self, url: str) -> str | None:
        """
        Load the paper's landing page and look for any <a> tag pointing to a PDF.
        Returns the first PDF href found, or None.
        """
        status = self.webscraper.load_url(url)
        if not status:
            return None
        if not self.webscraper.initialize_soup():
            return None

        soup = self.webscraper.soup
        for a in soup.find_all("a", href=True):
            href: str = a["href"]
            if href.lower().endswith(".pdf") or "pdf" in href.lower():
                # Make absolute if relative
                if href.startswith("http"):
                    return href
                # Basic relative absolute (good enough for most cases)
                from urllib.parse import urljoin
                return urljoin(url, href)

        return None

    def search_and_download(self, search: SearchInput) -> DownloadSummary:
        """
        Full pipeline:
          search enrich PDF links download all return summary.
        """
        print(f"\nSearching for: {search.query}")
        papers = self.search(search)
        print(f"Found {len(papers)} results. Resolving PDF links...")

        papers = self.enrich_pdf_links(papers)
        linked = sum(1 for p in papers if p.get("pdf_link"))
        print(f"PDF links resolved: {linked}/{len(papers)}\n")

        summary = self.downloader.download_all(papers, query=search.query)
        summary.print_report()
        return summary

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _parse_meta(self, result_div) -> tuple[str | None, int | None]:
        """Extract authors string and publication year from a gs_a div."""
        meta_tag = result_div.find("div", class_="gs_a")
        if not meta_tag:
            return None, None

        text = meta_tag.get_text()

        # Year is a 4-digit number between 1900 and 2099
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        year = int(year_match.group()) if year_match else None

        # Authors are before the first " - "
        parts = text.split(" - ")
        authors = parts[0].strip() if parts else None

        return authors, year

    def _extract_inline_pdf(self, result_div) -> str | None:
        """
        Scholar sometimes shows a [PDF] link in .gs_or_ggsm next to the result.
        """
        pdf_div = result_div.find("div", class_="gs_or_ggsm")
        if not pdf_div:
            return None
        a = pdf_div.find("a", href=True)
        if a and ".pdf" in a["href"].lower():
            return a["href"]
        return None