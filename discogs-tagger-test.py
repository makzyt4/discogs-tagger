import unittest

from lyrics import LirycsSearcher

class SearchTest(unittest.TestCase):
    def test(self):
        searcher = LyricsSearcher("radiohead")
        searcher.load()
        lyrics = searcher.search_lyrics("treefingers")
        self.assertEqual(lyrics, "Instrumental")
