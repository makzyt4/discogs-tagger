import requests

from bs4 import BeautifulSoup


class WebCrawler:
    def __init__(self):
        self.header = {
            'User-Agent': 'Discogs Tagger User Agent 1.0'
        }

    def get_response(self, url):
        return requests.get(url, headers=self.header)

    def get_soup(self, url):
        return BeautifulSoup(self.get_response(url).text, "html.parser")
