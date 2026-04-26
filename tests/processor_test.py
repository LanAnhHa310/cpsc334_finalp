from library.processor.processor import Processor

def test_load_papers_success():
    p = Processor()
    assert p.load_papers([{"title": "Water shortage and income inequality"}]) == True

def test_load_papers_bad_input():
    p = Processor()
    assert p.load_papers("not a list") == False

def test_find_duplicates():
    p = Processor()
    p.load_papers([
        {"title": "Deep Learning"},
        {"title": "machine learning"},
        {"title": "deep learning"} # duplicate     
    ])
    dupes = p.find_duplicates()
    assert len(dupes) == 1
    assert dupes[0]["title"] == "deep learning"

def test_find_duplicates_none():
    p = Processor()
    p.load_papers = ([{"title": "Paper a"}, {"title": "Paper b"}])
    assert p.find_duplicates() == []

def test_find_duplicates_empty():
    p = Processor()
    p.load_papers([])
    assert p.find_duplicates() == []
