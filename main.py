import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
 
from library.paper_finder.paper_finder import PaperFinder
from library.search_input.search_input import parse_cli_args
 
 
def main():
    print("Hello from cpsc334-finalp searching branch!")
    p = PaperFinder()
    search_input = parse_cli_args()
 
    # pipeline: search, resolve PDF links, download, report
    summary = p.search_and_download(search_input)

    if summary.results and not summary.succeeded and not summary.skipped:
        sys.exit(1)
 
 
if __name__ == "__main__":
    main()
 