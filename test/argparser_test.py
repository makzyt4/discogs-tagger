import unittest

from discogstagger.argparser import ArgumentParser

class ValidURLTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertTrue(parser["urlvalid"])
        self.assertEqual(parser["url"], url)


class InvalidURLTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertEqual(parser["url"], url)
        self.assertFalse(parser["urlvalid"])


class NotDiscogsURLTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        args = ['-u', url]
        parser = ArgumentParser(args)
        self.assertFalse(parser["urlvalid"])
        self.assertEqual(parser["url"], url)

class InteractiveIsTrueTest(unittest.TestCase):
    def test(self):
        args = ['-i']
        parser = ArgumentParser(args)
        self.assertTrue(parser["interactive"])
