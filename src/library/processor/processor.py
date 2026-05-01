# Process class: for processing and cleaning data after downloading
# List of scraped papers results
import csv
import os
import logging
from library.file_naming.file_naming import make_results_folder, sanitize_title

logger = logging.getLogger(__name__)
class Processor:
    def __init__(self):
        self.papers = []
    
    #Load a list of papers dicts into the processor
    def load_papers(self, papers: list) -> bool:
        if not isinstance(papers, list):
            logger.warning("load_papers: expected a list, got %s", type(papers).__name__)
            return False
        self.papers = papers
        logger.info("load_papers: loaded %d papers", len(papers))
        return True
    
    # Returns papers that are duplicated based on 
    # matching title (case-insensitive)
    def find_duplicates(self) -> list:
        seen = {}
        duplicates = []
        for paper in self.papers:
            title = paper.get("title", "").strip().lower()
            if title in seen:
                duplicates.append(paper)
            else:
                seen[title] = paper
        logger.info("find_duplicates: found %d duplicate(s)", len(duplicates))
        return duplicates
    
    # remove the duplicated paper (case-insenstive)
    def remove_duplicates(self) -> list:
        dupes = self.find_duplicates()
        self.papers = [p for p in self.papers if p not in dupes]
        logger.info("remove_duplicates: %d paper(s) remaining after removal", len(self.papers))
        return self.papers
    
    # export to csv files
    def to_csv(self, query: str) -> bool:
        if not self.papers:
            logger.warning("to_csv: no papers to export")   
            return False
        
        folder = make_results_folder()
        filepath = os.path.join(folder, sanitize_title(query) + ".csv")

        fields = ["title", "authors", "year", "url", "pdf_link"]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader() 
            writer.writerows(self.papers)
        logger.info("to_csv: exported %d papers to %s", len(self.papers), filepath)
        return True

    def filter_by_year(self, start: int, end: int) ->list:
        self.papers = [p for p in self.papers if start <= (p.get("year") or 0) <= end]
        return self.papers