import unittest

from discogstagger.crawler import WebCrawler, Artist, Release


class ValidArtistInfoTest(unittest.TestCase):
    def test(self):
        artist = Artist('https://www.discogs.com/artist/277139-Hash-Jar-Tempo')
        artist.load()
        self.assertEqual(artist.name, 'Hash Jar Tempo')
        self.assertEqual(len(artist.albumviews), 2)
        self.assertEqual(artist.albumviews[0]['title'], 'Well Oiled')
        self.assertEqual(artist.albumviews[0]['label'], 'Drunken Fish Records')
        self.assertEqual(artist.albumviews[0]['year'], '1997')


class UppercaseArtistTest(unittest.TestCase):
    def test(self):
        artist = Artist('https://www.discogs.com/artist/307-Boards-Of-Canada')
        artist.load()
        self.assertEqual(artist.name, 'Boards of Canada')
        self.assertEqual(artist.albumviews[2]['title'],
                         'Music Has the Right to Children')
        self.assertEqual(artist.albumviews[2]['label'], 'Warp Records')


class ValidMasterReleaseInfoTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/CW-Vrtacek-Victory-Through-Grace/' +\
              'release/770038'
        artist_url = 'https://www.discogs.com/artist/268908-CW-Vrtacek'
        release = Release(url)
        release.load()
        self.assertEqual(release.albumartist, 'C.W. Vrtacek')
        self.assertEqual(release.title, 'Victory Through Grace')
        self.assertEqual(release.label, 'Leisure Time Records')
        self.assertEqual(release.format, 'Vinyl')
        self.assertEqual(release.style, 'Avantgarde')
        self.assertEqual(release.year, '1981')
