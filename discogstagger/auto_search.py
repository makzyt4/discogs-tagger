from discogstagger.search import Search
from discogstagger.crawler import Release, Artist


class AutoSearch(Search):
    def __init__(self, parser, settings):
        Search.__init__(self)
        self.parser = parser
        self.settings = settings

    def search_release(self):
        print("Loading URL :: {}".format(self.parser['url']))
        self.release = Release(self.parser['url'])
        self.release.load()
        self.artist = Artist(self.base_url + self.release.artist_link)
        self.artist.load()
