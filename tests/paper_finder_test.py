from library.paper_finder.paper_finder import PaperFinder
from library.search_input.search_input import SearchInput

def test_keyword_creation_a() -> None:
    pf = PaperFinder()
    search = SearchInput(query="Hello, World!")
    success = pf.get_seach_keywords(search) == ["Hello", "World"]
    assert success == True

def test_keyword_creation_b() -> None:
    pf = PaperFinder()
    search = SearchInput(query="abcdef")
    success = pf.get_seach_keywords(search) == ["abcdef"]
    assert success == True

def test_keyword_creation_c() -> None:
    pf = PaperFinder()
    search = SearchInput(query="123.456.789")
    success = pf.get_seach_keywords(search) == ["123456789"]
    assert success == True

def test_keyword_creation_d() -> None:
    pf = PaperFinder()
    search = SearchInput(query="!@#$%^&*")
    success = pf.get_seach_keywords(search) == [""]
    assert success == True

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

def test_url_creation_start_year() -> None:
    pf = PaperFinder()
    search = SearchInput(query="Hello, World!", year_start=2017)
    success = pf.create_url(search) == "https://scholar.google.com/scholar?q=Hello+World&as_ylo=2017"
    assert success == True

def test_url_creation_end_year() -> None:
    pf = PaperFinder()
    search = SearchInput(query="Hello, World!", year_end=2022)
    success = pf.create_url(search) == "https://scholar.google.com/scholar?q=Hello+World&as_yhi=2022"
    assert success == True

def test_url_creation_start_year_and_end_year() -> None:
    pf = PaperFinder()
    search = SearchInput(query="Hello, World!", year_start=2017, year_end=2022)
    success = pf.create_url(search) == "https://scholar.google.com/scholar?q=Hello+World&as_ylo=2017&as_yhi=2022"
    assert success == True