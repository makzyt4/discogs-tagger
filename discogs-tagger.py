#/usr/bin/python
import discogstagger.argparser
import discogstagger.crawler
import discogstagger.lyrics
import discogstagger.settings
import discogstagger.tagger
import discogstagger.renamer
import discogstagger.auto_search
import discogstagger.interactive_search
import sys


if __name__ == '__main__':
    base_url = discogstagger.crawler.WebCrawler().base_url
    parser = discogstagger.argparser.ArgumentParser()
    settings = discogstagger.settings.SettingsManager()

    if not settings.load():
        print("Couldn't find settings file. Creating new one...")
        settings.generate()
    else:
        print("Loading settings file...")

    print(settings.settings)

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
        autosearch = discogstagger.auto_search.AutoSearch(parser, settings)
        autosearch.search_release()
        if autosearch.ask_if_ok():
            autosearch.tag_files()
    elif parser['interactive']:
        interactive_search = discogstagger.interactive_search.InteractiveSearch(
            parser, settings)
        interactive_search.search_artist()
        interactive_search.choose_release()
        if interactive_search.ask_if_ok():
            interactive_search.tag_files()
