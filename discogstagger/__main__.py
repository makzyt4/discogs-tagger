#!/usr/bin/python
import sys

from discogstagger.argparser import ArgumentParser
from discogstagger.crawler import WebCrawler, Artist, Release
from discogstagger.lyrics import LyricsSearcher
from discogstagger.settings import SettingsManager
from discogstagger.tagger import Tagger
from discogstagger.renamer import FileRenamer
from discogstagger.auto_search import AutoSearch
from discogstagger.interactive_search import InteractiveSearch


def main():
    base_url = WebCrawler().base_url
    parser = ArgumentParser()
    settings = SettingsManager()

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
        autosearch = AutoSearch(parser, settings)
        autosearch.search_release()
        if autosearch.ask_if_ok():
            autosearch.tag_files()
    elif parser['interactive']:
        interactive_search = InteractiveSearch(parser, settings)
        interactive_search.search_artist()
        interactive_search.choose_release()
        if interactive_search.ask_if_ok():
            interactive_search.tag_files()


if __name__ == '__main__':
    main()
