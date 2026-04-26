import re
import os
import shutil

# Maximum allowed length for generated filenames/folders
MAX_FILENAME_LEN = 100

# Clean and format a string to be filesystem-safe
def sanitize_title(title: str) -> str:
    name = title.lower().strip()                                              
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", "_", name)   
    name = name.strip("_")          
    return name[:MAX_FILENAME_LEN]                                            

# Create output folder based on query name                           
def make_output_folder(query: str) -> str:                                    
    folder = os.path.join("output", "papers", sanitize_title(query))  # build folder path
    os.makedirs(folder, exist_ok=True)
    return folder 

def make_results_folder() -> str:
    folder = os.path.join("output", "results")
    os.makedirs(folder, exist_ok=True)
    return folder

def rename_pdf(src_path: str, title: str, query: str) -> str:
    folder = make_output_folder(query)
    new_name = sanitize_title(title) + ".pdf"
    dest_path = os.path.join(folder, new_name)
    shutil.copy2(src_path,dest_path)
    return dest_path
