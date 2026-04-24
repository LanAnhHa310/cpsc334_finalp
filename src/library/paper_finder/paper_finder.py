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

        return target_url

    def search(self, search : SearchInput) -> dict:
        target_url = self.create_url(search)
        self.webscraper.load_url()
        pass