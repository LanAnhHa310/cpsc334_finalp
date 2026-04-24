from library.paper_finder.paper_finder import PaperFinder

def test_url_creation_no_keyword() -> None:
    pf = PaperFinder()
    success = pf.create_url([]) == "https://scholar.google.com/scholar?q="
    assert success == True

def test_url_creation_one_keyword() -> None:
    pf = PaperFinder()
    success = pf.create_url(["hello"]) == "https://scholar.google.com/scholar?q=hello"
    assert success == True

def test_url_creation_two_keywords() -> None:
    pf = PaperFinder()
    success = pf.create_url(["hello", "world"]) == "https://scholar.google.com/scholar?q=hello+world"
    assert success == True

def test_url_creation_three_keywords() -> None:
    pf = PaperFinder()
    success = pf.create_url(["this", "is", "a"]) == "https://scholar.google.com/scholar?q=this+is+a"
    assert success == True