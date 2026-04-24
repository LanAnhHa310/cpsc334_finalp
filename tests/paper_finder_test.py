from library.paper_finder.paper_finder import PaperFinder
from library.search_input.search_input import SearchInput

def test_url_creation_no_keyword() -> None:
    pf = PaperFinder()
    search = SearchInput(query="")
    success = pf.create_url(search) == "https://scholar.google.com/scholar?q="
    assert success == True

def test_url_creation_one_keyword() -> None:
    pf = PaperFinder()
    search = SearchInput(query="hello")
    success = pf.create_url(search) == "https://scholar.google.com/scholar?q=hello"
    assert success == True

def test_url_creation_two_keywords() -> None:
    pf = PaperFinder()
    search = SearchInput(query="hello world")
    success = pf.create_url(search) == "https://scholar.google.com/scholar?q=hello+world"
    assert success == True

def test_url_creation_three_keywords() -> None:
    pf = PaperFinder()
    search = SearchInput(query="this is a")
    success = pf.create_url(search) == "https://scholar.google.com/scholar?q=this+is+a"
    assert success == True