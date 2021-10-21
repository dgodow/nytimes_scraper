import pytest
import re
from scraper import WebScraper
from bs4 import BeautifulSoup

URL = "https://www.nytimes.com/2020/09/02/opinion/remote-learning-coronavirus.html"

@pytest.fixture
def parser():
  return WebScraper(URL)

@pytest.fixture
def parsed_html():
  scraper = WebScraper(URL)
  return scraper._get_article(URL)

class TestScraper:

  def test_get_article_retrieves_bs4(self, parser):

    test_parsed_html = parser._get_article(parser.url)
    assert isinstance(test_parsed_html, BeautifulSoup)
  
  def test_parse_title(self, parser, parsed_html):

    test_title = parser._parse_article_title(parsed_html)    
    
    assert isinstance(test_title, str)
    assert len(test_title) > 0

  def test_parse_content(self, parser, parsed_html):

    test_content = parser._parse_article_content(parsed_html)
    html_regex = re.compile("/<\\/?[a-z][\\s\\S]*>/")

    assert isinstance(test_content, str)
    assert len(test_content) > 0
    assert re.match(html_regex, test_content) is None

  def test_parse_byline(self, parser, parsed_html):

    test_byline = parser._parse_byline(parsed_html)

    assert isinstance(test_byline, str)
    assert len(test_byline) > 0
    assert test_byline[0:3] != "By "

  def test_publication_date(self, parser, parsed_html):

    test_publication_date = parser._parse_original_publication_date(parsed_html)

    # TODO: The rest of the test