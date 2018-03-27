import unittest

from discogstagger.lyrics import LyricsSearcher

class ValidSearchTest(unittest.TestCase):
    def test(self):
        searcher = LyricsSearcher("radiohead")
        searcher.load()
        lyrics = searcher.search_lyrics("treefingers")
        self.assertEqual(lyrics, " Instrumental\n")

class InvalidArtistTest(unittest.TestCase):
    def test(self):
        searcher = LyricsSearcher("dfsgfvfsd")
        self.assertEqual(searcher.load(), False)

if __name__ == "__main__":
    ValidSearchTest().test()
    InvalidArtistTest().test()
