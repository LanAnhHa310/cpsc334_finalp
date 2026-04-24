import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest
from library.search_input.search_input import parse_input, SearchInput

def test_basic_query():
    result = parse_input("child development psychology")
    assert result.query == "child development psychology"

def test_default_results():
    result = parse_input("machine learning")
    assert result.num_results == 20

def test_custom_results():
    result = parse_input("machine learning", num_results=50)
    assert result.num_results == 50

def test_year_range():
    result = parse_input("ABC", year_start=2018, year_end=2024)
    assert result.year_start == 2018
    assert result.year_end == 2024

def test_whitespace_cleaned():
    result = parse_input("  machine   learning  ")
    assert result.query == "machine learning"

def test_min_length_query():
    result = parse_input("ai")
    assert result.query == "ai"

def test_returns_search_input():
    result = parse_input("deep learning")
    assert isinstance(result, SearchInput)