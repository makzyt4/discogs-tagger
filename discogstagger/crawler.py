import requests

from bs4 import BeautifulSoup
from discogstagger.wordprocessor import WordProcessor
from collections import defaultdict


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
        for tr in cards.find_all('tr', {'class': 'card'}):
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
            self.format = info['format']\
                .replace('\n', '')\
                .replace(' ', '')\
                .split(',')[0]\
                .strip()
        else:
            self.format = ''
        if 'label' in info:
            self.label = info['label'].split('–')[0][:-1].strip()
        else:
            self.label = ''
        if 'year' in info:
            self.year = info['year']
        else:
            self.year = info['released'].split(' ')[-1]
        self.style = info['style'].split(',')[0]
        self.subreleases = self._get_subreleases()
        self.tracklist = self._get_tracklist()

    def _get_title(self):
        profile_title_h1 = self.soup.find('h1', {'id': 'profile_title'})
        title = profile_title_h1.find_all('span', {'itemprop': 'name'})[1]
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
        for div in profile.find_all('div'):
            if 'head' in div['class']:
                key = div.text[:-1].lower()
            elif 'content' in div['class']:
                info[key] = WordProcessor().lowercase_shorts(div.text)
        return info

    def _get_subreleases(self):
        subreleases = []
        if not self.is_master:
            return subreleases
        cards = self.soup.find('table', {'id': 'versions'})
        for tr in cards.find_all('tr', {'class': 'card'}):
            title_td = tr.find('td', {'class': 'title'})
            label_td = tr.find('td', {'class': 'label'})
            title = title_td.find('a').text
            format = title_td.find('span', {'class': 'format'}).text
            link = title_td.find('a')['href']
            label = label_td.find('a').text
            country = tr.find('td', {'class': 'country'}).text
            year = tr.find('td', {'class': 'year'}).text
            subreleases.append({
                'title': WordProcessor().lowercase_shorts(title),
                'format': format,
                'link': link,
                'country': country,
                'label': WordProcessor().lowercase_shorts(label),
                'year': year
            })
        return subreleases

    def _get_tracklist(self):
        tracklist = []
        if self.is_master:
            return tracklist
        section_content = self.soup.find('div', {'class': 'section_content'})
        for tr in section_content.find_all('tr', {'class': 'tracklist_track'}):
            tr.find('blockquote').extract()
            trackpos = tr.find('td', {'class', 'tracklist_track_pos'}).text
            tracktitle = tr.find('td', {'class', 'tracklist_track_title'}).text
            tracklist.append({
                'number': trackpos,
                'title': WordProcessor().lowercase_shorts(tracktitle)
            })
        self._translate_tracklist(tracklist)
        return tracklist

    def _translate_tracklist(self, tracklist):
        vinyl = True if tracklist[0]['number'].startswith('A') else False
        multvin = True if ord(tracklist[-1]['number'][0]) > ord('B') else False
        if not vinyl:
            if '-' in tracklist[0]['number']:
                disc_max = tracklist[-1]['number'].split('-')[0]
                disc_max = '{:02}'.format(int(disc_max))
                disc_dict = defaultdict(int)
                for i in range(len(tracklist)):
                    (disc, num) = tracklist[i]['number'].split('-')
                    disc = '{:02}'.format(int(disc))
                    num = '{:02}'.format(int(num))
                    disc_dict[disc] += 1
                    tracklist[i]['disc'] = disc
                    tracklist[i]['number'] = num
                    tracklist[i]['disctotal'] = disc_max
                for i in range(len(tracklist)):
                    tracktotal = disc_dict[tracklist[i]['disc']]
                    tracklist[i]['tracktotal'] = '{:02}'.format(tracktotal)
            else:
                for i in range(len(tracklist)):
                    tracklist[i]['disc'] = ''
                    tracklist[i]['disctotal'] = ''
                    tracklist[i]['tracktotal'] = '{:02}'.format(len(tracklist))
                    tracklist[i]['number'] = '{:02}'.format(i + 1)
        elif multvin:
            disc_max = tracklist[-1]['number'][0]
            disc_dict = defaultdict(int)
            for i in range(len(tracklist)):
                discnum = self._disc_signum(tracklist[i]['number'][0])
                disc = '{:02}'.format(discnum)
                disc_dict[disc] += 1
                tracklist[i]['disc'] = disc
                if tracklist[i]['number'][1:] == '':
                    tracklist[i]['number'] = '01'
                else:
                    tracklist[i]['number'] = '{:02}'.format(
                        int(tracklist[i]['number'][1:]))
                tracklist[i]['disctotal'] = '{:02}'.format(
                    self._disc_signum(disc_max))
            for i in range(len(tracklist)):
                tracktotal = disc_dict[tracklist[i]['disc']]
                tracklist[i]['tracktotal'] = '{:02}'.format(tracktotal)
        else:
            for i in range(len(tracklist)):
                tracklist[i]['disc'] = ''
                tracklist[i]['disctotal'] = ''
                tracklist[i]['tracktotal'] = '{:02}'.format(len(tracklist))
                tracklist[i]['number'] = '{:02}'.format(i + 1)

    def _disc_signum(self, c):
        return ((ord(c) - ord('A')) // 2) + 1
