import argparse

from discogstagger.urlvalidator import URLValidator

class ArgumentParser:
    def __getitem__(self, item):
        return self.options[item]

    def __init__(self, args):
        self.options = {
            'url': None,
            'urlvalid': False,
            'interactive': False,
            'ambiguous': False
        }
        self.parser = argparse.ArgumentParser(
            description='Simple script that tags your music files with album '
                        'metadata from Discogs database.')
        self.parser.add_argument('files', metavar='file', nargs='*',
            help='file(s) you want to tag')
        self.parser.add_argument('-u', '--url',
            help='Discogs release url. Important: it must not be master '
                 'release!')
        self.parser.add_argument('-i', '--interactive',
            help='Option that allows user to manually choose artist and album'
                 ' release.', action='store_true')
        args = self.parser.parse_args(args)
        self.options['url'] = args.url
        self.options['urlvalid'] = URLValidator().validate(args.url)
        self.options['interactive'] = args.interactive
        if self.options['urlvalid'] and self.options['interactive']:
            self.options['ambiguous'] = True
