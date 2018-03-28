import discogstagger.argparser
import discogstagger.crawler
import discogstagger.lyrics
import discogstagger.settings
import sys


def ask_if_continue():
    while True:
        choice = input("Do you want to continue? (Y/n): ")
        if choice == "Y":
            number_of_files = min(len(tl), number_of_files)
            return True
        elif choice == "n":
            return False
        else:
            print("Wrong input. Enter uppercase 'Y' or lowercase 'n'.")


if __name__ == "__main__":
    base_url = discogstagger.crawler.WebCrawler().base_url
    parser = discogstagger.argparser.ArgumentParser()
    settings = discogstagger.settings.SettingsManager()

    if not settings.load():
        print("Couldn't find settings file. Creating new one...")
        settings.generate()
    else:
        print("Loading settings file...")

    if len(parser['files']) == 0:
        print("You haven't selected any files!")
        sys.exit(3)

    if parser['ambiguous']:
        print("There cannot be both interactive and URL option! Choose one.")
        sys.exit(1)

    if parser['url'] is not None:
        if not parser['urlvalid']:
            print("Given URL is not a valid Discogs release URL. Example: " +
                  "'https://www.discogs.com/Mr-James-Barth-AD-Knockin-Boots-Vol-2-Of-2/release/2'")
            sys.exit(2)
        print("Loading URL :: {}".format(parser['url']))
        release = discogstagger.crawler.Release(parser['url'])
        release.load()
        artist = discogstagger.crawler.Artist(base_url + release.artist_link)
        release.print_summary()
        if len(parser['files']) != len(release.tracklist):
            print("WARNING: The files number and tracklist length don't match.")
            if not ask_if_continue():
                print("Exiting...")
                sys.exit(0)
            for f in parser['files']:
                searcher = discogstagger.lyrics.LyricsSearcher(artist.name)
                tag_file(filename, artist, track, settings, searcher)
