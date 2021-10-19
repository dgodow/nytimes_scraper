# NYTimes Web Scraper

This app extracts various data -- author, content, publication date, etc. -- from a New York Times article given a NYTimes.com URL. It's a toy project to fulfill the requirements of this codementor.io exercise: https://www.codementor.io/projects/tool/web-scraper-to-get-news-article-content-atx32d46qe.

# Usage

The scraper only works via the command line. 

- Clone the repo onto your machine
- Navigate to the repo's directory in your terminal
- Copy-paste a valid NYTimes URL into scraper.py
- Execute the script via `python3 scraper.py`

The scraper object will store all of the relevant data for your article (byline, content, etc.); you can output this to your terminal by printing the scraper object in the main() function.