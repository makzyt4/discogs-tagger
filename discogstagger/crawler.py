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


class Release:
    def __init__(self, url):
        self.url = url

    def load(self):
        self.soup = WebCrawler().get_soup(self.url)
        self.is_master = True
        self.title = self._get_title()
        self.albumartist = self._get_albumartist()
        info = self._get_info()
        if 'format' in info:
            self.is_master = False
            self.format = info['format'].split(',')[0]
        else:
            self.format = ''
        if 'label' in info:
            self.label = info['label'].split('–')[0][:-1].strip()
        else:
            self.label = ''
        if 'year' in info:
            self.year = info['year']
        else:
            self.year = info['released']
        self.style = info['style'].split(',')[0]

    def _get_title(self):
        profile_title_h1 = self.soup.find('h1', {'id': 'profile_title'})
        title = profile_title_h1.findAll('span', {'itemprop': 'name'})[1]
        return WordProcessor().lowercase_shorts(title.text)

    def _get_albumartist(self):
        profile_title_h1 = self.soup.find('h1', {'id': 'profile_title'})
        artist = profile_title_h1.find('span', {'itemprop': 'byArtist'})
        link_artist = artist.find('a')
        if link_artist != None:
            return WordProcessor().lowercase_shorts(link_artist.text)
        return WordProcessor().lowercase_shorts(artist.text)

    def _get_info(self):
        info = {}
        profile = self.soup.find('div', {'class': 'profile'})
        key = ''
        for div in profile.findAll('div'):
            if 'head' in div['class']:
                key = div.text[:-1].lower()
            elif 'content' in div['class']:
                info[key] = WordProcessor().lowercase_shorts(div.text)
        return info
