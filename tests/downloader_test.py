import os
import pytest
from unittest.mock import MagicMock, patch
from library.downloader.downloader import Downloader, DownloadResult

# tmp_path is a built-in pytest fixture that creates a temporary folder
# that gets cleaned up automatically after each test

@pytest.fixture
def downloader():
    return Downloader(max_retries=2, retry_delay=0)  # delay=0 so tests run fast


# --- No PDF link ---
def test_no_pdf_link_returns_error(downloader, tmp_path):
    paper = {"title": "Some Paper", "pdf_link": None}
    result = downloader._download_one(paper, str(tmp_path))
    assert result.success is False
    assert result.error == "No PDF link available"


# --- File already exists ---
def test_skips_existing_file(downloader, tmp_path):
    (tmp_path / "some_paper.pdf").write_bytes(b"fake pdf")
    paper = {"title": "Some Paper", "pdf_link": "http://example.com/paper.pdf"}
    result = downloader._download_one(paper, str(tmp_path))
    assert result.skipped is True


# --- Successful download ---
def test_successful_download(downloader, tmp_path):
    mock_response = MagicMock()
    mock_response.content = b"%PDF-fake content"
    mock_response.raise_for_status = MagicMock()

    with patch("library.downloader.downloader.requests.get", return_value=mock_response):
        paper = {"title": "Good Paper", "pdf_link": "http://example.com/good.pdf"}
        result = downloader._download_one(paper, str(tmp_path))

    assert result.success is True
    assert result.saved_path is not None
    assert os.path.exists(result.saved_path)


# --- Duplicate content blocked ---
def test_duplicate_hash_is_skipped(downloader, tmp_path):
    mock_response = MagicMock()
    mock_response.content = b"%PDF-identical content"
    mock_response.raise_for_status = MagicMock()

    with patch("library.downloader.downloader.requests.get", return_value=mock_response):
        paper1 = {"title": "Paper One", "pdf_link": "http://example.com/one.pdf"}
        paper2 = {"title": "Paper Two", "pdf_link": "http://example.com/two.pdf"}
        downloader._download_one(paper1, str(tmp_path))
        result = downloader._download_one(paper2, str(tmp_path))

    assert result.skipped is True


# --- 404 does not retry ---
def test_404_does_not_retry(downloader, tmp_path):
    mock_response = MagicMock()
    mock_response.status_code = 404
    http_error = Exception("404")
    http_error.response = mock_response

    with patch("library.downloader.downloader.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = \
            __import__("requests").HTTPError(response=mock_response)
        paper = {"title": "Missing Paper", "pdf_link": "http://example.com/missing.pdf"}
        result = downloader._download_one(paper, str(tmp_path))

    assert result.success is False
    assert mock_get.call_count == 1  # only tried once, no retries


# --- Retries on connection error ---
def test_retries_on_connection_error(downloader, tmp_path):
    with patch("library.downloader.downloader.requests.get") as mock_get:
        mock_get.side_effect = __import__("requests").ConnectionError("failed")
        paper = {"title": "Flaky Paper", "pdf_link": "http://example.com/flaky.pdf"}
        result = downloader._download_one(paper, str(tmp_path))

    assert result.success is False
    assert mock_get.call_count == 2  # tried max_retries=2 times


# --- download_all summary ---
def test_download_all_summary(downloader, tmp_path):
    mock_response = MagicMock()
    mock_response.content = b"%PDF-content"
    mock_response.raise_for_status = MagicMock()

    papers = [
        {"title": "Paper A", "pdf_link": "http://example.com/a.pdf"},
        {"title": "Paper B", "pdf_link": None},
    ]

    with patch("library.downloader.downloader.requests.get", return_value=mock_response):
        with patch("library.downloader.downloader.make_output_folder", return_value=str(tmp_path)):
            summary = downloader.download_all(papers, query="test query")

    assert len(summary.succeeded) == 1
    assert len(summary.failed) == 1