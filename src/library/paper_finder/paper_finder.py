from library.webscraper.webscraper import Webscraper
from library.search_input.search_input import SearchInput
import string

SCHOLAR_URL = "https://scholar.google.com/scholar?q="

class PaperFinder:
    def __init__(self):
        self.webscraper = Webscraper()

    ## Strips keywords of special characters for searching.
    def get_seach_keywords(self, search : SearchInput) -> list:
        clean_query : str = search.query.translate(str.maketrans('', '', string.punctuation))
        keywords = clean_query.split(" ")
        return keywords

    ## Creates a url to scrape based on the search data.
    def create_url(self, search : SearchInput) -> str:
        target_url : str = SCHOLAR_URL

        keywords = self.get_seach_keywords(search)
        keyword_count : int = len(keywords)
        for index, keyword in enumerate(keywords):
            target_url += keyword
            if keyword_count != index + 1:
                target_url += "+"

        if search.year_start:
            target_url += "&as_ylo=" + str(search.year_start)
        if search.year_end:
            target_url += "&as_yhi=" + str(search.year_end)

        return target_url

    ## DO NOT Automate testing this - scholar will detect & block us
    def search(self, search : SearchInput) -> list[dict]:
        search_results : list[dict] = []
        
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

        # Each result is in a div with class "gs_r gs_or gs_scl"
        results = soup.find_all("div", class_="gs_r")

        for result in results:
            # Title and link are in the h3.gs_rt anchor tag
            title_tag = result.find("h3", class_="gs_rt")
            if title_tag:
                link_tag = title_tag.find("a")
                if link_tag:
                    search_results.append(
                        {
                            "title": link_tag.get_text(),
                            "link": link_tag.get("href"),
                            "year" : None,
                            "pdf_link" : None,
                            "authors" : None
                        }
                    )

        return search_results