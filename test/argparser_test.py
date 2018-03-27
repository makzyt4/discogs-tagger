import unittest

from discogstagger.argparser import ArgumentParser

class ValidURLTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertTrue(parser["urlvalid"])
        self.assertEqual(parser["url"], url)
        self.assertFalse(parser['ambiguous'])


class InvalidURLTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertEqual(parser["url"], url)
        self.assertFalse(parser["urlvalid"])
        self.assertFalse(parser['ambiguous'])


class NotDiscogsURLTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertFalse(parser["urlvalid"])
        self.assertEqual(parser["url"], url)
        self.assertFalse(parser['ambiguous'])

class InteractiveIsTrueTest(unittest.TestCase):
    def test(self):
        args = ['-i']
        parser = ArgumentParser(args)
        self.assertTrue(parser["interactive"])
        self.assertFalse(parser['ambiguous'])

class InteractiveAndURLTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        args = ['-i', '-u', url]
        self.assertTrue(parser['ambiguous'])
