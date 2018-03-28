from discogstagger.crawler import WebCrawler, Artist, Release
from discogstagger.tagger import Tagger
from discogstagger.renamer import FileRenamer
from discogstagger.lyrics import LyricsSearcher


class Search:
    def __init__(self):
        self.base_url = WebCrawler().base_url

    def ask_if_continue(self, text):
        while True:
            choice = input(text + " (Y/n): ")
            if choice == "Y":
                return True
            elif choice == "n":
                return False
            else:
                print("Wrong input. Enter uppercase 'Y' or lowercase 'n'.")

    def connect_to_lyric_wikia(self):
        if self.settings['tag-lyrics'] == 'true':
            print("Connecting to Lyrics Wikia...")
            if self.searcher.load():
                print("Found artist.")
            else:
                print("Couldn't find that artist.")

    def ask_if_ok(self):
        self.release.print_summary()
        if len(self.parser['files']) != len(self.release.tracklist):
            print("WARNING: The files number and tracklist length don't match.")
        if not self.ask_if_continue("Do you want to start tagging the files?"):
            print("Exiting...")
            return False
        return True

    def tag_files(self):
        self.searcher = LyricsSearcher(self.artist.name)
        self.connect_to_lyric_wikia()
        self.tagger = Tagger(self.artist, self.release,
                             self.settings, self.searcher)
        self.renamer = FileRenamer(self.settings['format'])
        files = self.parser['files']
        for i in range(len(files)):
            print("Tagging :: {}".format(files[i]))
            result = self.tagger.tag_file(files[i], self.release.tracklist[i])
            if result == False:
                print("Could not tag a file: '{}'".format(files[i]))
            print("Renaming :: {}".format(files[i]))
            self.renamer.rename_file(
                files[i], self.release.tracklist[i], self.release, self.artist)
