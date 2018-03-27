import unittest

from discogstagger.argparser import ArgumentParser

class ValidUrlTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertTrue(parser["urlvalid"])
        self.assertEqual(parser["url"], url)


class InvalidUrlTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertFalse(parser["urlvalid"])
        self.assertEqual(parser["url"], url)


class NotDiscogsReleaseUrlTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertFalse(parser["urlvalid"])
        self.assertEqual(parser["url"], url)
