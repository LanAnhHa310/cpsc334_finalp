from library.webscraper.webscraper import Webscraper

SCHOLAR_URL = "https://scholar.google.com/scholar?q="

class PaperFinder:
    def __init__(self):
        self.webscraper = Webscraper()

    def create_url(self, keywords : list) -> str:
        target_url : str = SCHOLAR_URL
        keyword_count : int = len(keywords)
        for index, keyword in enumerate(keywords):
            target_url += keyword
            if keyword_count != index + 1:
                target_url += "+"

        return target_url

    def search_by_keywords(self, keywords : list) -> dict:
        target_url = self.create_url(keywords)
        self.webscraper.load_url()
        pass