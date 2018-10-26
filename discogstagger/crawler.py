import requests
import urllib

from bs4 import BeautifulSoup
from collections import defaultdict
from discogstagger.wordprocessor import WordProcessor


class WebCrawler:
    def __init__(self):
        self.base_url = "https://discogs.com"
        self.header = {
            'User-Agent': 'Discogs Tagger User Agent 1.0'
        }

    def get_response(self, url):
        return requests.get(url, headers=self.header)

    def get_soup(self, url):
        return BeautifulSoup(self.get_response(url).text, 'html.parser')

    def search_artist(self, settings):
        artist_name = input("Enter artist name: ")
        artists = self.search_artists(artist_name)
        query_length = min(int(settings["artist-query-size"]), len(artists))
        for i in range(query_length):
            print("[{0:2}] {1}".format(i + 1, artists[i]['name']))
        print("-" * 80)
        while True:
            try:
                index = int(input("Enter index of artist: "))
                if index < 1 or index > len(artists):
                    print("Value out of range. Try again.")
                else:
                    break
            except ValueError:
                print("Wrong value. Please enter an integer.")
        print("-" * 80)
        artist = Artist(
            self.base_url + artists[index - 1]['link'] + "?sort=year%2Casc&limit=500&page=1")
        return artist

    def search_artists(self, artist_name):
        url = "https://www.discogs.com/search/?q={}&type=artist"\
            .format(urllib.parse.quote_plus(artist_name))
        soup = WebCrawler().get_soup(url)
        artists = []
        for x in soup.findAll("a", {"class": "search_result_title"}):
            artists.append({
                'name': WordProcessor().process(x.text),
                'link': x['href']}
            )
        return artists


class Artist:
    def __init__(self, url):
        self.url = url

    def load(self):
        self.soup = WebCrawler().get_soup(self.url)
        self.name = self._get_name()
        self.albumviews = self._get_albumviews()

    def print_summary(self, numbered=False):
        print(self.name)
        print('-' * 80)
        print(':: Discography ::')
        if numbered:
            i = 1
            for album in self.albumviews:
                print('[{:02}] {} ({}) <{}>'.format(
                    i, album['title'], ['year'], album['label']))
                i += 1
        else:
            print('{} ({}) <{}>'.format(
                album['title'], ['year'], album['label']))
        print('-' * 80)

    def _get_name(self):
        name = self.soup.find('h1', {'class': 'hide_mobile'}).text
        name = WordProcessor().process(name)
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
                'title': WordProcessor().process(title),
                'link': link,
                'label': WordProcessor().process(label),
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
        self.album_artist = self._get_album_artist()
        self.artist_link = self._get_artist_link()
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
        self.genre = info['genre'].split(',')[0]
        self.subreleases = self._get_subreleases()
        self.tracklist = self._get_tracklist()

    def print_summary(self, numbered=False):
        print('{} - {} ({})'.format(self.album_artist, self.title, self.year))
        print('Label: {}'.format(self.label))
        print('Format: {}'.format(self.format))
        print('Style: {}'.format(self.style))
        print('-' * 80)
        if self.is_master:
            print(":: Subreleases ::")
            if numbered:
                i = 1
                for sub in self.subreleases:
                    print('[{}] {} {} ({}) <{}>'.format(
                        i, sub['title'], sub['format'], sub['year'], sub['label']))
                    i += 1
            else:
                for sub in self.subreleases:
                    print('{} {} ({}) <{}>'.format(
                        sub['title'], sub['format'], sub['year'], sub['label']))

        else:
            print(":: Tracklist ::")
            for track in self.tracklist:
                if track['disc'] == '':
                    print('{} - {}'.format(track['number'], track['title']))
                else:
                    print('{}-{} - {}'.format(track['disc'], track['number'],
                                              track['title']))
        print('-' * 80)

    def _get_title(self):
        profile_title_h1 = self.soup.find('h1', {'id': 'profile_title'})
        print(profile_title_h1)
        #title = profile_title_h1.find_all('span', {'itemprop': 'name'})[1]
        title = profile_title_h1.find_all('span')[-1]
        return WordProcessor().process(title.text)

    def _get_artist_link(self):
        profile_title_h1 = self.soup.find('h1', {'id': 'profile_title'})
        print('============')
        print(profile_title_h1)
        artist = profile_title_h1.find('span', {'itemprop': 'byArtist'})
        if not artist:
            artist_link = profile_title_h1.find('a')['href']
        else:
            artist_link = artist.find('a')['href']
        return WordProcessor().process(artist_link)

    def _get_album_artist(self):
        profile_title_h1 = self.soup.find('h1', {'id': 'profile_title'})
        print(profile_title_h1)
        artist = profile_title_h1.find('span', {'itemprop': 'byArtist'})
        if not artist:
            artist = profile_title_h1.find('span')
        link_artist = artist.find('a')
        return WordProcessor().process(link_artist.text)

    def _get_info(self):
        info = {}
        profile = self.soup.find('div', {'class': 'profile'})
        key = ''
        for div in profile.find_all('div'):
            if 'head' in div['class']:
                key = div.text[:-1].lower()
            elif 'content' in div['class']:
                info[key] = WordProcessor().process(div.text)
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
                'title': WordProcessor().process(title),
                'format': format,
                'link': link,
                'country': country,
                'label': WordProcessor().process(label),
                'year': year
            })
        return subreleases

    def _get_tracklist(self):
        tracklist = []
        if self.is_master:
            return tracklist
        section_content = self.soup.find('div', {'class': 'section_content'})
        for tr in section_content.find_all('tr', {'class': 'tracklist_track'}):
            bq = tr.find('blockquote')
            if 'track_heading' in tr['class']:
                continue
            if bq is not None:
                bq.extract()
            trackpos = tr.find('td', {'class', 'tracklist_track_pos'}).text
            tracktitle = tr.find('td', {'class', 'tracklist_track_title'}).text
            tracklist.append({
                'number': trackpos,
                'title': WordProcessor().process(tracktitle)
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
                    tracklist[i]['number'] = '{:02}'.format(disc_dict[disc])
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
