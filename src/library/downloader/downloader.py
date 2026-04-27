import os
import time
import hashlib
import requests
from dataclasses import dataclass, field
from typing import Optional
from library.file_naming.file_naming import make_output_folder, sanitize_title

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Non-retryable HTTP status codes permanent failures
PERMANENT_ERRORS = {403, 404, 410}

# How long to wait between requests to avoid rate limiting
REQUEST_DELAY = 1.5  # seconds


@dataclass
class DownloadResult:
    """Tracks the outcome of a single PDF download attempt."""
    title:      str
    pdf_link:   Optional[str]
    saved_path: Optional[str] = None
    success:    bool          = False
    skipped:    bool          = False   # duplicate by hash or file already exists
    error:      Optional[str] = None

    def __str__(self):
        if self.success:
            return f"[OK]      {self.title} → {self.saved_path}"
        if self.skipped:
            return f"[SKIP]    {self.title} ({self.error or 'already exists'})"
        return f"[FAILED]  {self.title} — {self.error}"


@dataclass
class DownloadSummary:
    """Aggregate results from download_all()."""
    results:  list = field(default_factory=list)

    @property
    def succeeded(self):  return [r for r in self.results if r.success]
    @property
    def failed(self):     return [r for r in self.results if not r.success and not r.skipped]
    @property
    def skipped(self):    return [r for r in self.results if r.skipped]

    def print_report(self):
        print(f"\n{'='*60}")
        print(f"  Download Summary")
        print(f"   Success : {len(self.succeeded)}")
        print(f"   Failed  : {len(self.failed)}")
        print(f"   Skipped : {len(self.skipped)}")
        print(f"{'='*60}")
        if self.failed:
            print("\nFailed downloads:")
            for r in self.failed:
                print(f"   {r.title}: {r.error}")
        print()


class Downloader:
    """
    Downloads PDFs for a list of paper dicts produced by PaperFinder.search().

    Each dict is expected to have:
        "title"     : str
        "pdf_link"  : str | None

    Files are saved to output/papers/<query>/<sanitized_title>.pdf
    using the same folder/naming rules as file_naming.py.
    """

    def __init__(self, max_retries: int = 3, retry_delay: float = 2.0):
        self.max_retries   = max_retries
        self.retry_delay   = retry_delay
        self._seen_hashes: set[str] = set()

    def download_all(self, papers: list[dict], query: str) -> DownloadSummary:
        """
        Download PDFs for every paper in the list.

        Parameters
        ----------
        papers : list of dicts with pdf_link populated
        query  : original search query used to create the output folder

        Returns
        -------
        DownloadSummary with per-file DownloadResult objects
        """
        summary = DownloadSummary()
        output_folder = make_output_folder(query)

        for paper in papers:
            result = self._download_one(paper, output_folder)
            summary.results.append(result)
            print(str(result))
            time.sleep(REQUEST_DELAY)

        return summary

    def _download_one(self, paper: dict, output_folder: str) -> DownloadResult:
        title    = paper.get("title", "untitled")
        pdf_link = paper.get("pdf_link")

        # No link was resolved — nothing to download
        if not pdf_link:
            return DownloadResult(
                title=title, pdf_link=None,
                error="No PDF link available"
            )

        dest_path = os.path.join(output_folder, sanitize_title(title) + ".pdf")

        # Skip if already downloaded in a previous run
        if os.path.exists(dest_path):
            return DownloadResult(
                title=title, pdf_link=pdf_link,
                saved_path=dest_path, skipped=True,
                error="file already exists"
            )

        # Attempt download with retries
        last_error = "unknown error"
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(
                    pdf_link, headers=HEADERS,
                    timeout=30, stream=True
                )
                response.raise_for_status()

                content = response.content

                # Duplicate detection by MD5 hash (same PDF, different URL/title)
                content_hash = hashlib.md5(content).hexdigest()
                if content_hash in self._seen_hashes:
                    return DownloadResult(
                        title=title, pdf_link=pdf_link,
                        skipped=True, error="duplicate content (hash match)"
                    )
                self._seen_hashes.add(content_hash)

                with open(dest_path, "wb") as f:
                    f.write(content)

                return DownloadResult(
                    title=title, pdf_link=pdf_link,
                    saved_path=dest_path, success=True
                )

            except requests.HTTPError as e:
                status_code = e.response.status_code if e.response is not None else 0
                last_error  = f"HTTP {status_code}"
                if status_code in PERMANENT_ERRORS:
                    break

            except requests.ConnectionError:
                last_error = "connection error"

            except requests.Timeout:
                last_error = "request timed out"

            except Exception as e:
                last_error = str(e)
                break

            # Exponential backoff before next attempt
            if attempt < self.max_retries:
                wait = self.retry_delay * attempt
                print(f"  [retry {attempt}/{self.max_retries}] {title} waiting {wait}s")
                time.sleep(wait)

        return DownloadResult(
            title=title, pdf_link=pdf_link,
            error=f"{last_error} (after {self.max_retries} attempts)"
        )