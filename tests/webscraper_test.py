from library.webscraper.webscraper import Webscraper

def test_successful_url_load() -> None:
    w = Webscraper()
    success = w.load_url("https://google.com")
    assert success == True

def test_unsuccessful_url_load_site_down() -> None:
    w = Webscraper()
    success = w.load_url("https://google.com/thisisnotvalid")
    assert success == False

def test_unsuccessful_url_load_bad_url() -> None:
    w = Webscraper()
    success = w.load_url("THIS-IS-NOT-A-VALID-URL")
    assert success == False

def test_successful_soup_setup() -> None:
    w = Webscraper()
    w.html_data = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Page Title</title></head><body><h1>Hello World!</h1><p>This is a basic HTML page.</p></body></html>'
    success = w.initialize_soup()
    assert success == True

def test_unsuccessful_soup_setup_bad_data() -> None:
    w = Webscraper()
    w.html_data = 67
    success = w.initialize_soup()
    assert success == False

def test_unsuccessful_soup_setup_no_data() -> None:
    w = Webscraper()
    w.html_data = None
    success = w.initialize_soup()
    assert success == False
