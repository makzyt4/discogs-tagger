import unittest

from discogstagger.crawler import WebCrawler, Artist


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
        artist = Artist('https://www.discogs.com/artist/277139-Hash-Jar-Tempo')
        artist.load()
        self.assertEqual(artist.name, 'Hash Jar Tempo')
