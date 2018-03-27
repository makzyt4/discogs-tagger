import warnings
import urllib
warnings.filterwarnings("ignore", category=UserWarning)

from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
from discogstagger.crawler import WebCrawler


class LyricsSearcher:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.url_base = "http://lyrics.wikia.com"
        self.crawler = WebCrawler()
        url_search_fragment = "/wiki/Special:Search?query="
        artist_query = urllib.parse.quote_plus(artist_name)
        url = self.url_base + url_search_fragment + artist_query
        self.soup = self.crawler.get_soup(url)

    def load(self):
        li = self.soup.find("li", {"class": "result"})
        if li is None:
            return False
        first_artist = li.find_all("a", {"class": "result-link"})[0].text
        ratio = fuzz.ratio(first_artist, self.artist_name)
        if ratio < 60:
            return False
        first_link = li.find_all("a", {"class": "result-link"})[0]['href']
        self.soup = self.crawler.get_soup(first_link)
        return True

    def search_lyrics(self, track_title):
        ols = self.soup.find_all("ol")
        max_ratio = 0
        found = None
        for ol in ols:
            links = ol.find_all("a")
            for link in links:
                ratio = fuzz.ratio(track_title, link.text)
                if ratio > max_ratio:
                    max_ratio = ratio
                    found = {'link': link['href'], 'ratio': ratio}
        if found == None or found['ratio'] < 80:
            return ''
        track_soup = self.crawler.get_soup(self.url_base + found['link'])
        lyricbox = track_soup.find("div", {"class": "lyricbox"})
        if lyricbox is None:
            return ''
        for br in lyricbox.find_all("br"):
            br.replace_with("\n")
        return lyricbox.text
