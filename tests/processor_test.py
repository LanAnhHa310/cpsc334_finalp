from library.processor.processor import Processor
import os

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
    p.load_papers ([{"title": "Paper a"}, {"title": "Paper b"}])
    assert p.find_duplicates() == []

def test_find_duplicates_empty():
    p = Processor()
    p.load_papers([])
    assert p.find_duplicates() == []

def test_remove_duplicates():
    p = Processor()
    p.load_papers([
        {"title": "Deep Learning"},
        {"title": "machine learning"},
        {"title": "deep learning"} # duplicate   
    ])
    result = p.remove_duplicates()
    assert len(result) == 2
    assert len(p.papers) == 2 #confirm the update is in place

def test_to_csv_success():
    p = Processor()
    p.load_papers([{
        "title": "Deep Learning",
        "authors": "LeCun",
        "year": 2015, 
        "url": None, 
        "pdf_link": None
    }])
    assert p.to_csv("deep learning") == True
    assert os.path.exists(os.path.join("output", "results", "deep_learning.csv"))
def test_to_csv_empty():
    p = Processor()
    assert p.to_csv("deep learning") == False

def test_filter_by_year():
    p = Processor()
    p.load_papers([
        {"title": "Paper A", "year": 2019},
        {"title": "Paper B", "year": 2026},
    ])
    assert len(p.filter_by_year(2020, 2026)) == 1
    