from bs4 import BeautifulSoup
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

## Basic Webscraper class. Used to grab HTML data
## from specified websites.
class Webscraper:
    def __init__(self):
        self.html_data = None
        self.soup = None

    ## Loads the HTML data in a url to self.html_data.
    ## Returns true on successful load.
    def load_url(self, url : str) -> bool:
        try:
            response = requests.get(url, headers=HEADERS)
        except:
            return False

        # Check for success
        if response.ok:
            self.html_data = response.text
            return True
        else:
            return False
        
    ## Loads HTML data from self.html_data into.
    ## Returns true on successful load.
    def initialize_soup(self) -> bool:
        if self.html_data == None:
            return False
        
        try:
            self.soup = BeautifulSoup(self.html_data, "html.parser")
            return True
        except:
            return False