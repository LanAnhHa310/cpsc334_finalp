import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
 
from library.paper_finder.paper_finder import PaperFinder
from library.search_input.search_input import parse_cli_args
from library.processor.processor import Processor
from library.downloader.downloader import Downloader
 
 
def main():
    search_input = parse_cli_args()

    #1. Search
    finder = PaperFinder()
    papers = finder.search(search_input)

    if not papers:
        print("No result found!")
        sys.exit(1)
    
    #2. Processor
    processor = Processor()
    processor.load_papers(papers)
    processor.remove_duplicates()
    processor.to_csv(search_input.query)

    #3. Download 
    downloader = Downloader()
    summary = downloader.download_all(processor.papers, search_input.query)
    summary.print_report()
 
if __name__ == "__main__":
    main()
 