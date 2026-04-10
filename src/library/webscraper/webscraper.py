from bs4 import BeautifulSoup
import requests

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
            response = requests.get(url)
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