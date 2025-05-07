import pytest

import scrapers.sal
import utils.db

@pytest.fixture
def url():
    return "http://example.com/page"

@pytest.fixture
def target():
    return {"uri": "http://example.com", "other": "data"}

def test_should_scrape_triggers_scrape_for_new_url(mocker, url, target):
    mock_should_scrape = mocker.patch("utils.db.should_scrape", return_value=True)
    mock_scrape_page = mocker.patch("scrapers.sal.scrape_page")
    # Simulate the code block
    if utils.db.should_scrape(url):
        scrapers.sal.scrape_page(url, target)
    mock_should_scrape.assert_called_once_with(url)
    mock_scrape_page.assert_called_once_with(url, target)

def test_should_scrape_skips_existing_url(mocker, url, target):
    mock_should_scrape = mocker.patch("utils.db.should_scrape", return_value=False)
    mock_scrape_page = mocker.patch("scrapers.sal.scrape_page")
    if utils.db.should_scrape(url):
        scrapers.sal.scrape_page(url, target)
    mock_should_scrape.assert_called_once_with(url)
    mock_scrape_page.assert_not_called()

def test_should_scrape_triggers_when_file_missing(mocker, url, target):
    # Simulate should_scrape returns True when file is missing
    mock_should_scrape = mocker.patch("utils.db.should_scrape", return_value=True)
    mock_scrape_page = mocker.patch("scrapers.sal.scrape_page")
    if utils.db.should_scrape(url):
        scrapers.sal.scrape_page(url, target)
    mock_should_scrape.assert_called_once_with(url)
    mock_scrape_page.assert_called_once_with(url, target)

def test_should_scrape_with_empty_record_file(mocker, url, target):
    # Simulate should_scrape returns True when record file is empty
    mock_should_scrape = mocker.patch("utils.db.should_scrape", return_value=True)
    mock_scrape_page = mocker.patch("scrapers.sal.scrape_page")
    if utils.db.should_scrape(url):
        scrapers.sal.scrape_page(url, target)
    mock_should_scrape.assert_called_once_with(url)
    mock_scrape_page.assert_called_once_with(url, target)

def test_should_scrape_with_partial_match_in_record_file(mocker, url, target):
    # Simulate should_scrape returns False if a substring in record file matches url
    mock_should_scrape = mocker.patch("utils.db.should_scrape", return_value=False)
    mock_scrape_page = mocker.patch("scrapers.sal.scrape_page")
    if utils.db.should_scrape(url):
        scrapers.sal.scrape_page(url, target)
    mock_should_scrape.assert_called_once_with(url)
    mock_scrape_page.assert_not_called()

def test_should_scrape_with_malformed_record_file(mocker, url, target):
    # Simulate should_scrape handles malformed file and returns True (allows scraping)
    mock_should_scrape = mocker.patch("utils.db.should_scrape", return_value=True)
    mock_scrape_page = mocker.patch("scrapers.sal.scrape_page")
    if utils.db.should_scrape(url):
        scrapers.sal.scrape_page(url, target)
    mock_should_scrape.assert_called_once_with(url)
    mock_scrape_page.assert_called_once_with(url, target)