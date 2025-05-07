import pytest
from unittest.mock import MagicMock
import scrapers.pcl as pcl

@pytest.fixture
def target():
    return {
        'url': 'http://example.com/parent',
        'parent_container': '.parent',
        'child_anchor': 'a.child',
        'depth': 2,
        'uri': 'http://example.com',
        'page': {
            'title': 'h1.title',
            'content': 'div.content'
        }
    }

def make_bs4_element(href, title_text, content_text):
    # Simulate a bs4.element.Tag with .get_text and attribute access
    anchor = MagicMock()
    anchor.__getitem__.side_effect = lambda k: href if k == 'href' else None
    title = MagicMock()
    title.get_text.return_value = title_text
    content = MagicMock()
    content.get_text.return_value = content_text
    return anchor, title, content

def test_scrape_all_new_pages_with_keywords(mocker, target):
    # Mock parent page response
    parent_html = "<html></html>"
    parent_resp = MagicMock()
    parent_resp.text = parent_html
    parent_resp.status_code = 200
    parent_resp.raise_for_status = MagicMock()
    parent_resp.apparent_encoding = 'utf-8'
    parent_resp.encoding = None

    # Mock child page response
    child_html = "<html></html>"
    child_resp = MagicMock()
    child_resp.text = child_html
    child_resp.status_code = 200
    child_resp.raise_for_status = MagicMock()
    child_resp.apparent_encoding = 'utf-8'
    child_resp.encoding = None

    # Patch requests.get to return parent, then child responses
    mock_get = mocker.patch("requests.get", side_effect=[parent_resp, child_resp, child_resp])

    # Patch BeautifulSoup and its .css.select
    anchor1, title1, content1 = make_bs4_element('/child1', 'Title 1', 'Content with keyword')
    anchor2, title2, content2 = make_bs4_element('/child2', 'Title 2', 'Another content with keyword')
    soup_parent = MagicMock()
    soup_parent.css.select.return_value = [anchor1, anchor2]
    soup_child = MagicMock()
    soup_child.css.select_one.side_effect = [title1, content1]  # for first child
    soup_child2 = MagicMock()
    soup_child2.css.select_one.side_effect = [title2, content2]  # for second child

    mock_bs4 = mocker.patch("scrapers.pcl.BeautifulSoup", side_effect=[soup_parent, soup_child, soup_child2])

    # Patch should_scrape to always return True
    mocker.patch("utils.db.should_scrape", return_value=True)
    # Patch save_scrapped
    mock_save_scrapped = mocker.patch("utils.db.save_scrapped")
    # Patch summarize
    mocker.patch("utils.db.summarize", side_effect=lambda x: x[:300])
    # Patch check_content_has_keywords to always return (True, [...])
    mocker.patch("utils.keywords.check_content_has_keywords", return_value=(True, ['keyword']))
    # Patch save_markdown
    mock_save_md = mocker.patch("utils.md.save_markdown")

    pcl.get_child_pages(target)

    # Should call requests.get for parent and each child
    assert mock_get.call_count == 3
    # Should save scrapped for each child
    assert mock_save_scrapped.call_count == 2
    # Should save markdown for each child
    assert mock_save_md.call_count == 2
    # Should call summarize for each child content
    # Should call check_content_has_keywords for each child content

def test_skip_already_scrapped_urls(mocker, target):
    # Mock parent page response
    parent_resp = MagicMock()
    parent_resp.text = "<html></html>"
    parent_resp.status_code = 200
    parent_resp.raise_for_status = MagicMock()
    parent_resp.apparent_encoding = 'utf-8'
    parent_resp.encoding = None

    mocker.patch("requests.get", return_value=parent_resp)

    anchor1, _, _ = make_bs4_element('/child1', 'Title 1', 'Content')
    anchor2, _, _ = make_bs4_element('/child2', 'Title 2', 'Content')
    soup_parent = MagicMock()
    soup_parent.css.select.return_value = [anchor1, anchor2]
    mocker.patch("scrapers.pcl.BeautifulSoup", return_value=soup_parent)

    # Patch should_scrape to always return False (already scrapped)
    mock_should_scrape = mocker.patch("utils.db.should_scrape", return_value=False)
    mock_save_scrapped = mocker.patch("utils.db.save_scrapped")
    mock_save_md = mocker.patch("utils.md.save_markdown")

    pcl.get_child_pages(target)

    # Should call should_scrape for each child
    assert mock_should_scrape.call_count == 2
    # Should NOT call save_scrapped or save_markdown
    mock_save_scrapped.assert_not_called()
    mock_save_md.assert_not_called()

def test_ignore_pages_without_required_keywords(mocker, target):
    # Mock parent and child page responses
    parent_resp = MagicMock()
    parent_resp.text = "<html></html>"
    parent_resp.status_code = 200
    parent_resp.raise_for_status = MagicMock()
    parent_resp.apparent_encoding = 'utf-8'
    parent_resp.encoding = None

    child_resp = MagicMock()
    child_resp.text = "<html></html>"
    child_resp.status_code = 200
    child_resp.raise_for_status = MagicMock()
    child_resp.apparent_encoding = 'utf-8'
    child_resp.encoding = None

    mocker.patch("requests.get", side_effect=[parent_resp, child_resp])

    anchor, title, content = make_bs4_element('/child1', 'Title 1', 'Content without keywords')
    soup_parent = MagicMock()
    soup_parent.css.select.return_value = [anchor]
    soup_child = MagicMock()
    soup_child.css.select_one.side_effect = [title, content]
    mocker.patch("scrapers.pcl.BeautifulSoup", side_effect=[soup_parent, soup_child])

    mocker.patch("utils.db.should_scrape", return_value=True)
    mocker.patch("utils.db.save_scrapped")
    mocker.patch("utils.db.summarize")
    # Patch check_content_has_keywords to return False
    mocker.patch("utils.keywords.check_content_has_keywords", return_value=(False, ['keyword']))
    mock_save_md = mocker.patch("utils.md.save_markdown")

    pcl.get_child_pages(target)

    # Should NOT call save_markdown since keywords not found
    mock_save_md.assert_not_called()

def test_handle_http_request_failure(mocker, target):
    # Simulate requests.get raising an exception for parent page
    mocker.patch("requests.get", side_effect=Exception("Network error"))
    with pytest.raises(Exception, match="Network error"):
        pcl.get_child_pages(target)

    # Simulate requests.get raising an exception for child page
    parent_resp = MagicMock()
    parent_resp.text = "<html></html>"
    parent_resp.status_code = 200
    parent_resp.raise_for_status = MagicMock()
    parent_resp.apparent_encoding = 'utf-8'
    parent_resp.encoding = None

    anchor, _, _ = make_bs4_element('/child1', 'Title', 'Content')
    soup_parent = MagicMock()
    soup_parent.css.select.return_value = [anchor]
    mocker.patch("scrapers.pcl.BeautifulSoup", return_value=soup_parent)
    mocker.patch("utils.db.should_scrape", return_value=True)

    # Now requests.get will succeed for parent, fail for child
    mocker.patch("requests.get", side_effect=[parent_resp, Exception("Child page error")])

    with pytest.raises(Exception, match="Child page error"):
        pcl.get_child_pages(target)

def test_handle_missing_html_elements(mocker, target):
    # Mock parent and child page responses
    parent_resp = MagicMock()
    parent_resp.text = "<html></html>"
    parent_resp.status_code = 200
    parent_resp.raise_for_status = MagicMock()
    parent_resp.apparent_encoding = 'utf-8'
    parent_resp.encoding = None

    child_resp = MagicMock()
    child_resp.text = "<html></html>"
    child_resp.status_code = 200
    child_resp.raise_for_status = MagicMock()
    child_resp.apparent_encoding = 'utf-8'
    child_resp.encoding = None

    mocker.patch("requests.get", side_effect=[parent_resp, child_resp])

    anchor, _, _ = make_bs4_element('/child1', None, None)
    soup_parent = MagicMock()
    soup_parent.css.select.return_value = [anchor]
    soup_child = MagicMock()
    # Simulate select_one returning None for title and content
    soup_child.css.select_one.side_effect = [None, None]
    mocker.patch("scrapers.pcl.BeautifulSoup", side_effect=[soup_parent, soup_child])

    mocker.patch("utils.db.should_scrape", return_value=True)
    mocker.patch("utils.db.save_scrapped")
    mocker.patch("utils.db.summarize")
    mocker.patch("utils.keywords.check_content_has_keywords")
    mock_save_md = mocker.patch("utils.md.save_markdown")

    # Should raise AttributeError when trying to call get_text on None
    with pytest.raises(AttributeError):
        pcl.get_child_pages(target)

def test_handle_empty_required_keywords(mocker, target):
    # Mock parent and child page responses
    parent_resp = MagicMock()
    parent_resp.text = "<html></html>"
    parent_resp.status_code = 200
    parent_resp.raise_for_status = MagicMock()
    parent_resp.apparent_encoding = 'utf-8'
    parent_resp.encoding = None

    child_resp = MagicMock()
    child_resp.text = "<html></html>"
    child_resp.status_code = 200
    child_resp.raise_for_status = MagicMock()
    child_resp.apparent_encoding = 'utf-8'
    child_resp.encoding = None

    mocker.patch("requests.get", side_effect=[parent_resp, child_resp])

    anchor, title, content = make_bs4_element('/child1', 'Title', 'Content')
    soup_parent = MagicMock()
    soup_parent.css.select.return_value = [anchor]
    soup_child = MagicMock()
    soup_child.css.select_one.side_effect = [title, content]
    mocker.patch("scrapers.pcl.BeautifulSoup", side_effect=[soup_parent, soup_child])

    mocker.patch("utils.db.should_scrape", return_value=True)
    mocker.patch("utils.db.save_scrapped")
    mocker.patch("utils.db.summarize", side_effect=lambda x: x[:300])
    # Patch check_content_has_keywords to simulate empty required_words (should return True, [])
    mocker.patch("utils.keywords.check_content_has_keywords", return_value=(True, []))
    mock_save_md = mocker.patch("utils.md.save_markdown")

    pcl.get_child_pages(target)

    # Should still save markdown even if required_words is empty
    mock_save_md.assert_called_once()