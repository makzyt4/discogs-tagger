import unittest

from discogstagger.renamer import FileRenamer


class ValidTaggingReplace(unittest.TestCase):
    def test(self):
        text = '${tag1-}${tag2} - ${tag3}${ tag4}'
        renamer = FileRenamer(text)
        renamer.replace_tag('tag1', '01')
        renamer.replace_tag('tag2', '02')
        renamer.replace_tag('tag3', None)
        renamer.replace_tag('tag4', '')
        self.assertEqual(renamer.processed, '01-02 - ')
