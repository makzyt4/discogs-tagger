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
