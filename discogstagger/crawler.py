import requests

from bs4 import BeautifulSoup
from discogstagger.wordprocessor import WordProcessor


class WebCrawler:
    def __init__(self):
        self.header = {
            'User-Agent': 'Discogs Tagger User Agent 1.0'
        }

    def get_response(self, url):
        return requests.get(url, headers=self.header)

    def get_soup(self, url):
        return BeautifulSoup(self.get_response(url).text, 'html.parser')


class Artist:
    def __init__(self, url):
        self.url = url

    def load(self):
        self.soup = WebCrawler().get_soup(self.url)
        self.name = self._get_name()
        self.albumviews = self._get_albumviews()

    def _get_name(self):
        name = self.soup.find('h1', {'class': 'hide_mobile'}).text
        name = WordProcessor().lowercase_shorts(name)
        return name

    def _get_albumviews(self):
        cards = self.soup.find('table', {'id': 'artist'})
        albumviews = []
        for tr in cards.findAll('tr', {'class': 'card'}):
            title_td = tr.find('td', {'class': 'title'})
            label_td = tr.find('td', {'class': 'label'})
            title = title_td.find('a').text
            link = title_td.find('a')['href']
            label = label_td.find('a').text
            year = tr.find('td', {'class': 'year'}).text
            albumviews.append({
                'title': WordProcessor().lowercase_shorts(title),
                'link': link,
                'label': WordProcessor().lowercase_shorts(label),
                'year': year
            })
        return albumviews
