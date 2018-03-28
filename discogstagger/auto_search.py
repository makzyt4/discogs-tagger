import discogstagger.search


class AutoSearch(discogstagger.search.Search):
    def __init__(self, parser, settings):
        discogstagger.search.Search.__init__(self)
        self.parser = parser
        self.settings = settings

    def search_release(self):
        print("Loading URL :: {}".format(self.parser['url']))
        self.release = discogstagger.crawler.Release(self.parser['url'])
        self.release.load()
        self.artist = discogstagger.crawler.Artist(
            self.base_url + self.release.artist_link)
        self.artist.load()
        self.release.print_summary()

    def ask_if_ok(self):
        if len(self.parser['files']) != len(self.release.tracklist):
            print("WARNING: The files number and tracklist length don't match.")
        if not self.ask_if_continue("Do you want to start tagging the files?"):
            print("Exiting...")
            return False
        return True

    def tag_files(self):
        self.searcher = discogstagger.lyrics.LyricsSearcher(self.artist.name)
        self.connect_to_lyric_wikia()
        self.tagger = discogstagger.tagger.Tagger(
            self.artist, self.release, self.settings, self.searcher)
        self.renamer = discogstagger.renamer.FileRenamer(
            self.settings['format'])
        files = self.parser['files']
        for i in range(len(files)):
            print("Tagging :: {}".format(files[i]))
            result = self.tagger.tag_file(files[i], self.release.tracklist[i])
            if result == False:
                print("Could not tag a file: '{}'".format(files[i]))
            print("Renaming :: {}".format(files[i]))
            self.renamer.rename_file(
                files[i], self.release.tracklist[i], self.release, self.artist)

    def connect_to_lyric_wikia(self):
        if self.settings['tag-lyrics'] == 'true':
            print("Connecting to Lyrics Wikia...")
            if self.searcher.load():
                print("Found artist.")
            else:
                print("Couldn't find that artist.")
