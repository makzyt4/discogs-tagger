import unittest

from discogstagger.argparser import ArgumentParser
from discogstagger.urlvalidator import URLValidator

class ValidURLTest(unittest.TestCase):
    def test(self):
        url = 'https://www.discogs.com/Radiohead-The-Bends/release/368116'
        validator = URLValidator()
        self.assertTrue(validator.validate(url))


class InvalidURLTest(unittest.TestCase):
    def test(self):
        url = '<Invalid Url>'
        validator = URLValidator()
        self.assertFalse(validator.validate(url))


class NotDiscogsURLTest(unittest.TestCase):
    def test(self):
        url = 'http://google.com'
        validator = URLValidator()
        self.assertFalse(validator.validate(url))
