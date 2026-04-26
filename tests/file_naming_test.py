from library.file_naming.file_naming import sanitize_title, make_output_folder
import os

# test basic title formatting
def test_sanitize_title_basic():                                              
    assert sanitize_title("Deep Learning") == "deep_learning"

# test removal of special characters
def test_sanitize_title_special_chars():
    assert sanitize_title("A.I. & Machine-Learning!") == "ai_machinelearning"

# test max length truncation
def test_sanitize_title_truncate():                                           
    assert len(sanitize_title("a" * 200)) == 100

# test handling of extra spaces
def test_sanitize_title_extra_spaces():
    assert sanitize_title("  deep   learning  ") == "deep_learning"

# test folder creation
def test_make_output_folder():                                                
    path = make_output_folder("machine learning")
    assert os.path.isdir(path)