import unittest

from discogstagger.argparser import ArgumentParser
from discogstagger.urlvalidator import UrlValidator

class ValidUrlTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        self.assertTrue(UrlValidator.validate(url))


class InvalidUrlTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        self.assertTrue(UrlValidator.validate(url))


class NotDiscogsReleaseUrlTest(unittest.TestCase):
    def test(self):
        url = 'http://google.com'
        self.assertTrue(UrlValidator.validate(url))
