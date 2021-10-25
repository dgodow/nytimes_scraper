import datetime
from re import compile, match
from requests import get
from bs4 import BeautifulSoup, element

SITEMAP_RAW_URL = "https://www.nytimes.com/sitemap/"

class ArticleURLCrawler:

  def __init__(self, date):

    self.date = date
    self.urls = []
  
  def get_urls(self, date):

    urls = []
    date_string = date.strftime("%Y/%m/%d/")
    sitemap_url = SITEMAP_RAW_URL + date_string

    raw_sitemap_content = get(sitemap_url)
    parsed_sitemap_content = BeautifulSoup(raw_sitemap_content.text, "html.parser").find(id="site-content")
    regex_to_find_articles = compile("https:\\/\\/www\\.nytimes\\.com\\/[12]\d{3}\\/[0-9]{2}\\/[0123][0-9]\\/")

    for el in parsed_sitemap_content.descendants:
      if isinstance(el, element.Tag) and el.name == "a" and match(regex_to_find_articles, el["href"]) is not None: # Find only links that match the "article" pattern, not interactive features or videos.
        url = el["href"]
        urls.append(url)

    return urls

  def crawl(self):

    self.urls = self.get_urls(self.date)

def main():
  todays_date = datetime.date.today()
  crawler = ArticleURLCrawler(todays_date)
  crawler.crawl()
  
if __name__ == "__main__":
  main()