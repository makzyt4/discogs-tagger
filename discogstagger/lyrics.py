import warnings
import urllib
warnings.filterwarnings("ignore", category=UserWarning)

import fuzzywuzzy

from bs4 import BeautifulSoup
from crawler import WebCrawler


class LyricsSearcher:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.url_base = "http://lyrics.wikia.com"
        self.crawler = WebCrawler()
        url_search_fragment = "/wiki/Special:Search?query="
        artist_query = urllib.parse.quote_plus(artist_name)
        url = url_base + url_search_fragment + artist_query
        self.soup = self.crawler.get_soup(url)
