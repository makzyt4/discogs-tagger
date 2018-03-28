# discogs-tagger
Simple script that tags your music files with album metadata from Discogs database.

## Installation

Use these commands to obtain discogs-tagger and go into the script folder:

```
$ git clone https://github.com/makzyt4/discogs-tagger
$ cd discogs-tagger
```

Now using pip 3 freeze download the dependencies:

```
# pip freeze -r requirements.txt
```

Finally, copy (or move) the script to your enviromental path. For example, `/usr/bin`:

```
# mv discogs-tagger.py /usr/bin/discogs-tagger
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
