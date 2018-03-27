import unittest

from discogstagger.lyrics import LyricsSearcher

class SearchTest(unittest.TestCase):
    def test(self):
        searcher = LyricsSearcher("radiohead")
        searcher.load()
        lyrics = searcher.search_lyrics("treefingers")
        self.assertEqual(lyrics, " Instrumental\n")


if __name__ == "__main__":
    SearchTest().test()
