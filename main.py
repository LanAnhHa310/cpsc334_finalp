import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from library.paper_finder.paper_finder import PaperFinder
from library.search_input.search_input import *

def main():
    print("Hello from cpsc334-finalp searching branch!")
    p = PaperFinder()
    search_input = parse_cli_args()
    r = p.search(search_input)
    print(r)

if __name__ == "__main__":
    main()
