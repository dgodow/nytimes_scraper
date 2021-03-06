from requests import get
from bs4 import BeautifulSoup, element
from datetime import datetime
from sys import argv
from re import compile, search

class WebScraper:

  def __init__(self, url):

    # article URL; each instance of WebScraper only supports a single URL
    self.url = url

    self.headline = ''
    self.article_content = ''
    self.author_byline = ''
    self.original_pub_date = ''
    self.updated_date = ''

  def __str__(self):

    printable_content = []

    printable_content.append("TITLE: {0}\n".format(self.headline))
    printable_content.append("AUTHOR: {0}\n".format(self.author_byline))
    printable_content.append("PUBLICATION DATE: {0}\n\n".format(self.original_pub_date))
    printable_content.append("UPDATED DATE: {0}\n\n".format(self.updated_date))
    printable_content.append(self.article_content)

    return "".join(printable_content)
  
  def _validate_url(self, url):
    """
    Ensures that the user entered a correct NYTimes.com URL. The scraper does not support 
    mobile pages or non-articles (e.g., interactive visualizations), so these are considered invalid.
    """

    has_valid_protocol = compile("http:\\/\\/|https:\\/\\/")
    has_valid_nytimes_url = compile("nytimes.com\\/[12]\d{3}\\/[0-9]{2}\\/[0123][0-9]\\/")
    is_html_file = compile("\\.html$")

    if search(has_valid_protocol, url) is None or search(is_html_file, url) is None:
      raise ValueError("Invalid URL.")

    if search(has_valid_nytimes_url, url) is None:
      raise ValueError("Not a valid NYTimes URL. The scraper does not support mobile NYTimes articles. Please enter a NYTimes web address (e.g., beginning with 'www.nytimes.com', not 'mobile.nytimes.com'.)")
  
  def _is_headline(self, tag):

    return tag.has_attr("data-testid") and tag["data-testid"] == "headline"

  def _is_article_content(self, tag):

    return tag.has_attr("name") and tag["name"] == "articleBody"

  def _get_article(self, url):

    html_response = get(url)
    raw_html = html_response.text

    parsed_html = BeautifulSoup(raw_html, "html.parser")

    # Remove irrelevant content from article text; no easy way to do this in bs4 without looping twice 
    for el in parsed_html.find_all("figure"): # Irrelevant graphics; also needed to remove "Listen to This Op-Ed" text for opinion articles
      el.decompose()

    for el in parsed_html.find_all("em"): # Metadata about the article and links to other content, which will always be bolded/italicized in NYT style
      el.decompose()

    return parsed_html

  def _parse_article_title(self, parsed_html):

    headline_tag = parsed_html.find(self._is_headline)
    return headline_tag.contents[0]

  def _parse_article_content(self, parsed_html):
    
    raw_article_tag = parsed_html.find(self._is_article_content)
    raw_article_tag_content = raw_article_tag.descendants
    raw_parsed_article_content = []
    
    for el in raw_article_tag_content:

      if isinstance(el, element.Tag) and el.name == "p":
        raw_parsed_article_content.append("\n\n")

      if isinstance(el, element.NavigableString):
        raw_parsed_article_content.append(el)

    parsed_article_content = "".join(raw_parsed_article_content)

    return parsed_article_content

  def _parse_byline(self, parsed_html):

    raw_author_byline = parsed_html.find("meta", attrs={"name": "byl"})["content"]
    author_byline = raw_author_byline[3:] # remove "By" boilerplate at the start of this attribute

    return author_byline

  def _parse_original_publication_date(self, parsed_html):

    raw_pub_date = parsed_html.find("meta", property="article:published_time")["content"]
    formatted_date = datetime.strptime(raw_pub_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    return formatted_date

  def _parse_updated_date(self, parsed_html):

    raw_updated_date = parsed_html.find("meta", property="article:modified_time")["content"]
    formatted_date = datetime.strptime(raw_updated_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    return formatted_date

  def run(self):

    self._validate_url(self.url)
    
    parsed_html = self._get_article(self.url)

    self.headline = self._parse_article_title(parsed_html)
    self.article_content = self._parse_article_content(parsed_html)
    self.author_byline = self._parse_byline(parsed_html)
    self.original_pub_date = self._parse_original_publication_date(parsed_html)
    self.updated_date = self._parse_updated_date(parsed_html)

def main():
  url = argv[1]
  scraper = WebScraper(url)
  scraper.run()
  print(scraper)

if __name__ == "__main__":
  main()