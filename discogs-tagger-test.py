import unittest

from test.lyrics_test import *

if __name__ == "__main__":
    # Lyrics searcher tests
    ValidSearchTest().test()
    InvalidArtistTest().test()
    InvalidTrackTest().test()
