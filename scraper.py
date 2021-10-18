from requests import get
from bs4 import BeautifulSoup

class WebScraper:

  def __init__(self, url):

    self.url = url

    return

  def _is_headline(self, tag):

    return tag.has_attr("data-testid") and tag["data-testid"] == "headline"

  def run(self):

    res = get(self.url)
    raw_html = res.text

    parsed_html = BeautifulSoup(raw_html, "html.parser")

    # Parse article title -- distinguished by tag with data-testid='headline'
    headline_tag = parsed_html.find_all(self._is_headline)

    if len(headline_tag) > 1:
      raise RuntimeError("More than one headline returned")

    self.headline_content = headline_tag[0].contents[0]

    # TODO: Parse article content

    # TODO: Parse author

    # TODO: Parse updated data

    # TODO: Parse byline

def main():
  url = "https://www.nytimes.com/2020/09/02/opinion/remote-learning-coronavirus.html"
  scraper = WebScraper(url)
  scraper.run()

if __name__ == "__main__":
  main()