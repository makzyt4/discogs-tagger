import unittest

from discogstagger.argparser import ArgumentParser


class ValidURLTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        args = ['-u', url, 'abc']
        parser = ArgumentParser(args)
        self.assertTrue(parser["urlvalid"])
        self.assertEqual(parser["url"], url)
        self.assertFalse(parser['ambiguous'])


class InvalidURLTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        args = ['-u', url, 'abc']
        parser = ArgumentParser(args)
        self.assertEqual(parser["url"], url)
        self.assertFalse(parser["urlvalid"])
        self.assertFalse(parser['ambiguous'])


class NotDiscogsURLTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        args = ['-u', url, 'abc']
        parser = ArgumentParser(args)
        self.assertFalse(parser["urlvalid"])
        self.assertEqual(parser["url"], url)
        self.assertFalse(parser['ambiguous'])


class InteractiveIsTrueTest(unittest.TestCase):
    def test(self):
        args = ['-i', 'abc']
        parser = ArgumentParser(args)
        self.assertTrue(parser["interactive"])
        self.assertFalse(parser['ambiguous'])


class InteractiveAndURLTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        args = ['-i', '-u', url, 'abc']
        parser = ArgumentParser(args)
        self.assertTrue(parser['ambiguous'])


class FilesAndInteractiveTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        args = ['-u', url, 'file1.flac', 'file2.flac']
        parser = ArgumentParser(args)
        self.assertFalse(parser['ambiguous'])
        self.assertEqual(parser['files'], ['file1.flac', 'file2.flac'])
