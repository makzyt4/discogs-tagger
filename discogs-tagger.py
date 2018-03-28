import discogstagger.argparser
import discogstagger.crawler
import discogstagger.lyrics
import discogstagger.settings
import sys

if __name__ == "__main__":
    parser = discogstagger.argparser.ArgumentParser(sys.argv)
    settings = discogstagger.settings.SettingsManager()

    if not settings.load():
        print("Couldn't find settings file. Creating new one...")
        settings.generate()
    else:
        print("Loading settings file...")

    if parser['ambiguous']:
        print("There cannot be both interactive and URL option! Choose one.")
        sys.exit(1)

    if parser['url'] is not None:
        print("Loading URL :: {}".format(parser['url']))
        release = discogstagger.crawler.Release(parser['url'])
        release.load()
        release.print_summary()
