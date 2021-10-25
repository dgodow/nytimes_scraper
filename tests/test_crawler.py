import pytest
from re import compile, match
from requests import get
from bs4 import BeautifulSoup, element
from nytimes_scraper.src.nytimes_scraper.url_crawler import ArticleURLCrawler, SITEMAP_RAW_URL

@pytest.fixture
def crawler():
  crawler = ArticleURLCrawler(SITEMAP_RAW_URL)
  crawler.crawl()
  return crawler

def test_get_urls(crawler):

  assert len(crawler.urls) > 1