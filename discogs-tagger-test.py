import unittest

import test.lyrics_test
import test.argparser_test
import test.urlvalidator_test

if __name__ == '__main__':
    # Lyrics searcher tests
    test.lyrics_test.ValidSearchTest().test()
    test.lyrics_test.InvalidArtistTest().test()
    test.lyrics_test.InvalidTrackTest().test()

    # Argument parser tests
    test.argparser_test.ValidURLTest().test()
    test.argparser_test.InvalidURLTest().test()
    test.argparser_test.NotDiscogsURLTest().test()

    # URL validator tests
    test.urlvalidator_test.ValidURLTest().test()
    test.urlvalidator_test.InvalidURLTest().test()
    test.urlvalidator_test.NotDiscogsURLTest().test()
