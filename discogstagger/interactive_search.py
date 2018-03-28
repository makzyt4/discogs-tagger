from discogstagger.search import Search
from discogstagger.crawler import WebCrawler, Artist, Release


class InteractiveSearch(Search):
    def __init__(self, parser, settings):
        Search.__init__(self)
        self.parser = parser
        self.settings = settings

    def search_artist(self):
        self.artist = WebCrawler().search_artist(self.settings)
        self.artist.load()

    def choose_release(self):
        masters = self.artist.albumviews
        for i in range(len(masters)):
            print("[{0:3}] {1}".format(i + 1, masters[i]['title']))
        print('-' * 80)
        while True:
            try:
                index = int(input("Enter index of master release: "))
                if index < 1 or index > len(masters):
                    print("Value out of range. Try again.")
                else:
                    break
            except ValueError:
                print("Wrong value. Please enter an integer.")
        print('-' * 80)
        self.release = Release(self.base_url + masters[index - 1]['link'])
        self.release.load()
        if not self.release.is_master:
            print("Found no subreleases.")
            return
        subreleases = self.release.subreleases
        for i in range(len(subreleases)):
            title = subreleases[i]['title']
            year = subreleases[i]['year']
            format = subreleases[i]['format']
            label = subreleases[i]['label']
            print("[{:3}] {} ({}) - {}, {}".format(i + 1, title, year,
                                                   format, label))
        print('-' * 80)
        while True:
            try:
                index = int(input("Enter index of subrelease release: "))
                if index < 1 or index > len(subreleases):
                    print("Value out of range. Try again.")
                else:
                    break
            except ValueError:
                print("Wrong value. Please enter an integer.")
        print('-' * 80)
        self.release = Release(self.base_url + subreleases[index - 1]['link'])
        self.release.load()

    def connect_to_lyric_wikia(self):
        if self.settings['tag-lyrics'] == 'true':
            print("Connecting to Lyrics Wikia...")
            if self.searcher.load():
                print("Found artist.")
            else:
                print("Couldn't find that artist.")
