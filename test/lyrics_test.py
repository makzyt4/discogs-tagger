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
        searcher = LyricsSearcher("<Invalid Artist Name>")
        self.assertFalse(searcher.load())


class InvalidTrackTest(unittest.TestCase):
    def test(self):
        searcher = LyricsSearcher("radiohead")
        searcher.load()
        lyrics = searcher.search_lyrics("<Invalid Track Title>")
        self.assertEqual(lyrics, "")
