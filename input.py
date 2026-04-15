
# defining keyword input format:
    # plain text search string
    # 2- 256 characters and not empty
    # limits: 1-200 results, valid year range


import re
import argparse
from dataclasses import dataclass, field
from typing import Optional

# constants
MIN_QUERY_LEN   = 2
MAX_QUERY_LEN   = 256
DEFAULT_RESULTS = 20
MIN_RESULTS     = 1
MAX_RESULTS     = 200



# data
@dataclass
class SearchInput:
    """validated, search parameters."""
    query:        str
    num_results:  int            = DEFAULT_RESULTS
    year_start:   Optional[int]  = None
    year_end:     Optional[int]  = None
    raw_input:    str            = field(default="", repr=False)
 
    def __str__(self):
        parts = [f'query="{self.query}"', f"results={self.num_results}"]
        if self.year_start:
            parts.append(f"from={self.year_start}")
        if self.year_end:
            parts.append(f"to={self.year_end}")
        return f"SearchInput({', '.join(parts)})"


# validation 

def _clean_query(raw: str) -> str:
    """remove extra whitespace, collapse internal runs to single spaces"""
    return re.sub(r"\s+", " ", raw.strip())
 
 
def _validate_query(query: str) -> str:
    if len(query) < MIN_QUERY_LEN:
        raise ValueError(
            f"Query too short (min {MIN_QUERY_LEN} chars). Got: {query!r}"
        )
    if len(query) > MAX_QUERY_LEN:
        raise ValueError(
            f"Query too long (max {MAX_QUERY_LEN} chars). Got {len(query)} chars."
        )
    return query
 
 
def _validate_results(n: int) -> int:
    if not (MIN_RESULTS <= n <= MAX_RESULTS):
        raise ValueError(
            f"--results must be between {MIN_RESULTS} and {MAX_RESULTS}. Got: {n}"
        )
    return n
 
 
def _validate_years(start: Optional[int], end: Optional[int]):
    import datetime
    current_year = datetime.date.today().year
    for label, yr in [("--start", start), ("--end", end)]:
        if yr is not None and not (1900 <= yr <= current_year):
            raise ValueError(f"{label} must be between 1900 and {current_year}. Got: {yr}")
    if start and end and start > end:
        raise ValueError(f"--start ({start}) cannot be after --end ({end}).")
 
# api

def parse_input(
    query:       str,
    num_results: int           = DEFAULT_RESULTS,
    year_start:  Optional[int] = None,
    year_end:    Optional[int] = None,
) -> SearchInput:
    """
    Validate and normalize user supplied search parameters
 
    Parameters
    ----------
    query       : Raw search string from the user.
    num_results : How many Scholar results to fetch.
    year_start  : Optional earliest publication year.
    year_end    : Optional latest  publication year.
 
    Returns
    -------
    SearchInput dataclass ready for the scraper.
 
    Raises
    ------
    ValueError on any invalid input.
    """
    raw = query
    query = _clean_query(query)
    query = _validate_query(query)
    num_results = _validate_results(num_results)
    _validate_years(year_start, year_end)
 
    return SearchInput(
        query=query,
        num_results=num_results,
        year_start=year_start,
        year_end=year_end,
        raw_input=raw,
    )
 

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="scholar_scraper",
        description="Search Google Scholar and export results cvs later.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "query",
        type=str,
        help='Search string. Use quotes for multi-word queries: "machine learning"',
    )
    p.add_argument(
        "--results",
        type=int,
        default=DEFAULT_RESULTS,
        metavar="N",
        help=f"Number of results to fetch (default: {DEFAULT_RESULTS}, max: {MAX_RESULTS})",
    )
    p.add_argument(
        "--start",
        type=int,
        default=None,
        metavar="YEAR",
        help="Filter: earliest publication year (e.g. 2015)",
    )
    p.add_argument(
        "--end",
        type=int,
        default=None,
        metavar="YEAR",
        help="Filter: latest publication year  (e.g. 2024)",
    )
    return p
 
 
def parse_cli_args() -> SearchInput:
    """Parse sys.argv and return a validated SearchInput."""
    parser = build_arg_parser()
    args = parser.parse_args()
    return parse_input(
        query=args.query,
        num_results=args.results,
        year_start=args.start,
        year_end=args.end,
    )



if __name__ == "__main__":
    result = parse_cli_args()
    print(result)