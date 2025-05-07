import os
import pytest
from utils.db import should_scrape, summarize, save_scrapped

@pytest.fixture
def test_file():
    return "db/test_scrapped.txt"

@pytest.fixture(autouse=True)
def cleanup_test_file(test_file):
    # Setup: ensure test file doesn't exist before each test
    if os.path.exists(test_file):
        os.remove(test_file)
    yield
    # Teardown: clean up test file after each test
    if os.path.exists(test_file):
        os.remove(test_file)

def test_should_scrape_new_url(test_file):
    """Test that should_scrape returns True for a new URL"""
    url = "http://example.com/new-page"
    assert should_scrape(url, test_file) is True

def test_should_scrape_existing_url(test_file):
    """Test that should_scrape returns False for an existing URL"""
    url = "http://example.com/existing-page"
    
    # First, create the file with the URL
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    with open(test_file, 'w') as f:
        f.write(f"{url}\n")
    
    assert should_scrape(url, test_file) is False

def test_should_scrape_partial_match(test_file):
    """Test that should_scrape returns False when URL contains a substring from the file"""
    url = "http://example.com/very/long/path"
    substring = "example.com"
    
    # Create file with substring
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    with open(test_file, 'w') as f:
        f.write(f"{substring}\n")
    
    assert should_scrape(url, test_file) is False

def test_should_scrape_no_match(test_file):
    """Test that should_scrape returns True when URL doesn't match any entry"""
    url = "http://example.com/new-page"
    
    # Create file with different URL
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    with open(test_file, 'w') as f:
        f.write("http://different.com/page\n")
    
    assert should_scrape(url, test_file) is True

def test_should_scrape_empty_file(test_file):
    """Test that should_scrape returns True when file exists but is empty"""
    url = "http://example.com/new-page"
    
    # Create empty file
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    with open(test_file, 'w') as f:
        pass
    
    assert should_scrape(url, test_file) is True

def test_summarize_short_text():
    """Test that summarize returns the full text when it's shorter than 300 characters"""
    text = "This is a short text"
    assert summarize(text) == text

def test_summarize_long_text():
    """Test that summarize truncates text longer than 300 characters"""
    # Create a text longer than 300 characters
    long_text = "a" * 400
    result = summarize(long_text)
    assert len(result) == 300
    assert result == long_text[:300]

def test_summarize_empty_text():
    """Test that summarize handles empty text"""
    assert summarize("") == ""

def test_save_scrapped_new_file(test_file):
    """Test that save_scrapped creates a new file and saves the URL"""
    url = "http://example.com/new-page"
    save_scrapped(url, test_file)
    
    assert os.path.exists(test_file)
    with open(test_file, 'r') as f:
        content = f.read().strip()
        assert content == url

def test_save_scrapped_append_to_existing(test_file):
    """Test that save_scrapped appends to existing file"""
    url1 = "http://example.com/first-page"
    url2 = "http://example.com/second-page"
    
    # Save first URL
    save_scrapped(url1, test_file)
    
    # Save second URL
    save_scrapped(url2, test_file)
    
    # Check both URLs are in the file
    with open(test_file, 'r') as f:
        content = f.read().strip().split('\n')
        assert len(content) == 2
        assert url1 in content
        assert url2 in content

def test_save_scrapped_creates_directory(test_file):
    """Test that save_scrapped creates the directory if it doesn't exist"""
    # Use a path with a non-existent directory
    custom_file = "db/custom/test_scrapped.txt"
    url = "http://example.com/new-page"
    
    # Ensure the directory doesn't exist
    if os.path.exists(os.path.dirname(custom_file)):
        os.rmdir(os.path.dirname(custom_file))
    
    save_scrapped(url, custom_file)
    
    assert os.path.exists(custom_file)
    with open(custom_file, 'r') as f:
        content = f.read().strip()
        assert content == url
    
    # Cleanup
    os.remove(custom_file)
    os.rmdir(os.path.dirname(custom_file)) 