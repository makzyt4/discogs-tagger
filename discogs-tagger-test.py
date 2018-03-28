import unittest

import test.lyrics_test
import test.argparser_test
import test.urlvalidator_test
import test.crawler_test


def show_progress(done, todo):
    length = 78
    i = int((done / todo) * length)
    print('[', end='')
    for j in range(i):
        print('+', end='')
    for j in range(length - i):
        print('-', end='')
    print('] ', end='')
    print('{}/{}'.format(done, todo), end='\r')


if __name__ == '__main__':
    tests = (
        # Lyrics searcher tests
        test.lyrics_test.ValidSearchTest(),
        test.lyrics_test.InvalidArtistTest(),
        test.lyrics_test.InvalidTrackTest(),

        # # Argument parser tests
        test.argparser_test.ValidURLTest(),
        test.argparser_test.InvalidURLTest(),
        test.argparser_test.NotDiscogsURLTest(),
        test.argparser_test.InteractiveIsTrueTest(),
        test.argparser_test.InteractiveAndURLTest(),
        test.argparser_test.FilesAndInteractiveTest(),

        # # URL validator tests
        test.urlvalidator_test.ValidURLTest(),
        test.urlvalidator_test.InvalidURLTest(),
        test.urlvalidator_test.NotDiscogsURLTest(),

        # # Discogs web crawling tests
        test.crawler_test.ValidArtistInfoTest(),
        test.crawler_test.UppercaseArtistTest(),
        test.crawler_test.ValidMasterReleaseInfoTest(),
        test.crawler_test.SubreleasesTest(),
        test.crawler_test.TracklistSingleVinylTest(),
        test.crawler_test.TracklistDoubleVinylTest(),
        test.crawler_test.TracklistTripleCDTest(),
        test.crawler_test.TracklistHeadlinesTest(),
    )

    i = 0
    show_progress(i, len(tests))
    for test in tests:
        test.test()
        i += 1
        show_progress(i, len(tests))
    print("\n100% of tests passed")
