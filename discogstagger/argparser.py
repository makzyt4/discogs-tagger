import argparse

class ArgumentParser:
    def __init__(self, args):
        self.parser = argparse.ArgumentParser(
            description='Simple script that tags your music files with album ' +
                        'metadata from Discogs database.')
        self.parser.add_argument('files', metavar='file', nargs='+',
            help='file(s) you want to tag')
        self.parser.add_argument('-u', '--url=', type=str,
            help='Discogs release url. Important: it must not be master ' +
                 'release!')
        self.parser.add_argument('-i', '--interactive', type=str,
            help='Option that allows user to manually choose artist and album' +
                 ' release.', action='store_true')
        self.parser.parse_args(args)
