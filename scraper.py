from requests import get
from bs4 import BeautifulSoup, element
from re import compile

class WebScraper:

  def __init__(self, url):

    # article URL; each instance of WebScraper only supports a single URL
    self.url = url

    # final parsed data from the article
    self.headline = ''
    self.article_content = ''
    self.author_byline = ''
    self.original_pub_date = ''

    return

  def _is_headline(self, tag):

    return tag.has_attr("data-testid") and tag["data-testid"] == "headline"

  def _is_article_content(self, tag):

    return tag.has_attr("name") and tag["name"] == "articleBody"

  def run(self):

    res = get(self.url)
    raw_html = res.text

    parsed_html = BeautifulSoup(raw_html, "html.parser")

    # Remove irrelevant content from article text
    parsed_html.figure.decompose() # Audio content
    for el in parsed_html.find_all("em"): # Metadata about the article and links to other content, which will always be bolded/italicized in NYT style
      el.decompose()

    # Parse article title -- distinguished by tag with data-testid='headline'
    headline_tag = parsed_html.find_all(self._is_headline)

    if len(headline_tag) > 1:
      raise RuntimeError("More than one headline returned")

    self.headline = headline_tag[0].contents[0]

    # Parse article content
    raw_article_tag = parsed_html.find_all(self._is_article_content)

    if len(raw_article_tag) > 1:
      raise RuntimeError("More than one article content tag returned")

    raw_article_tag_content = raw_article_tag[0].descendants
    raw_parsed_article_content = []
    
    for el in raw_article_tag_content:

      # TODO: if the element is a <p> tag, add a newline to preserve the readability of the text.

      if isinstance(el, element.NavigableString):
        raw_parsed_article_content.append(el)

    parsed_article_content = "".join(raw_parsed_article_content)
    self.article_content = parsed_article_content

    # Parse author byline
    raw_author_byline = parsed_html.find("span", class_=compile("last-byline"))
    author_byline = ''
    
    for el in raw_author_byline.descendants:
      if isinstance(el, element.NavigableString):
        author_byline = el

    self.author_byline = author_byline

    # Parse original publication date
    original_pub_date = parsed_html.find("meta", property="article:published_time")["content"]
    self.original_pub_date = original_pub_date

    # TODO: Parse updated publication date, if applicable

def main():
  url = "https://www.nytimes.com/2020/09/02/opinion/remote-learning-coronavirus.html"
  scraper = WebScraper(url)
  scraper.run()

if __name__ == "__main__":
  main()