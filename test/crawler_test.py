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
        release = Release(url)
        release.load()
        self.assertEqual(release.albumartist, 'C.W. Vrtacek')
        self.assertEqual(release.title, 'Victory Through Grace')
        self.assertEqual(release.label, 'Leisure Time Records')
        self.assertEqual(release.format, 'Vinyl')
        self.assertEqual(release.style, 'Avantgarde')
        self.assertEqual(release.year, '1981')
        self.assertFalse(release.is_master)


class SubreleasesTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Scraping-Foetus-Off-The-Wheel-Nail/' +\
            'master/8240'
        release = Release(url)
        release.load()
        self.assertEqual(release.albumartist, 'Scraping Foetus Off the Wheel')
        self.assertEqual(release.title, 'Nail')
        self.assertEqual(release.label, '')
        self.assertEqual(release.format, '')
        self.assertEqual(release.style, 'New Wave')
        self.assertEqual(release.year, '1985')
        self.assertTrue(release.is_master)
        self.assertEqual(len(release.subreleases), 15)
        self.assertEqual(release.subreleases[0]['title'], 'Nail')
        self.assertEqual(release.subreleases[0]['format'], '(LP, Album)')
        self.assertEqual(release.subreleases[0]['label'], 'Self Immolation')
        self.assertEqual(release.subreleases[0]['country'], 'UK')
        self.assertEqual(release.subreleases[0]['year'], '1985')
        url = '/Scraping-Foetus-Off-The-Wheel-Nail/release/137848'
        self.assertEqual(release.subreleases[0]['link'], url)


class TracklistSingleVinylTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-Pablo-Honey/release/339574'
        release = Release(url)
        release.load()
        self.assertEqual(release.albumartist, 'Radiohead')
        self.assertEqual(release.title, 'Pablo Honey')
        self.assertEqual(release.label, 'Parlophone')
        self.assertEqual(release.format, 'Vinyl')
        self.assertEqual(release.style, 'Alternative Rock')
        self.assertEqual(release.year, '1993')
        self.assertFalse(release.is_master)
        self.assertEqual(len(release.tracklist), 12)
        self.assertEqual(release.tracklist[0]['number'], '01')
        self.assertEqual(release.tracklist[0]['disc'], '')
        self.assertEqual(release.tracklist[0]['tracktotal'], '12')
        self.assertEqual(release.tracklist[0]['disctotal'], '')
        self.assertEqual(release.tracklist[0]['title'], 'You')
