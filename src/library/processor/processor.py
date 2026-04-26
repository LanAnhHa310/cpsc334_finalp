# Process class: for processing and cleaning data after downloading
# List of scraped papers results

class Processor:
    def __init__(self):
        self.papers = []
    
    #Load a list of papers dicts into the processor
    def load_papers(self, papers: list) -> bool:
        if not isinstance(papers, list):
            return False
        self.papers = papers
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
        return duplicates
    
    # remove the duplicated paper (case-insenstive)
    def remove_duplicates(self) -> list:
        dupes = self.find_duplicates()
        self.papers = [p for p in self.papers if p not in dupes]
        return self.papers