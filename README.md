# discogs-tagger
Simple script that tags your music files with album metadata from Discogs database.

## Installation

Simply install it using pip:

```
# pip install discogs-tagger
```

## Usage

```
usage: discogs-tagger.py [-h] [-u URL] [-i] file [file ...]

Simple script that tags your music files with album metadata from Discogs
database.

positional arguments:
  file               file(s) you want to tag

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  Discogs release URL. Important: it must not be master
                     release!
  -i, --interactive  Option that allows user to manually choose artist and
                     album release.
```

To tag your files, with discogs-tagger you can choose one method of two. The first one is automatic search. You give the script `-u <url>` option and it'll automatically download all the info on the album. Important - it mustn't be master release! Only albums without subreleases. Example:

```
$ discogs-tagger -u https://www.discogs.com/Radiohead-OK-Computer/release/4950798 ~/Music/OkComputerDir/*.flac
```

The other way is interactive search. You must enter artists name and then the script will show you available artists to choose from, then you choose a master release and subrelease. Command:

```
$ discogs-tagger -i ~/Music/SomeMusicDir/*.flac
```

What's also important, you should always choose files, otherwise the script won't do anything.

### Settings file

When you first run discogs-tagger, it will create new file at `~/discogs-tagger.settings`. Example settings file looks like this:

```
format=${d-}${n} - ${t}
artist-query-size=5
tag-lyrics=true
genre-base=style
```

- format - it's the format of file names that are being tagged
- artist-query-size - decides how many artists will show up in interactive mode
- tag-lyrics - boolean, decides if the lyrics will be embedded in the files (it may lenghten the process of tagging)
- genre-base - decides what Discogs tag it uses to describe genre: `style` or `genre`

#### File name formatting

These are tags used in file name formatting (`format` key in settings file):
- `${d}` - disc number
- `${dt}` - total disc number
- `${n}` - track number
- `${nt}` - total track number
- `${t}` - track title
- `${a}` - artist
- `${b}` - album artist

You can as well put special characters (but only valid for your filesystem). This
example

```
format=${d-}${n} - ${_t_}
```

may result in something like this: `01-05 - _Some title_`
