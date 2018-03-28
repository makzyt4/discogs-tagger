import mutagen


class Tagger:
    def __init__(self, release):
        self.release = release

    def tag_file(filename, artist, track, settings, searcher):
        audio = mutagen.File(file)

        # Clear all tags
        for key in audio.keys():
            audio[key] = ''

        audio["title"] = track['title']
        audio["album"] = self.release.title
        audio["artist"] = self.artist.name
        audio["date"] = self.release.year
        audio["genre"] = self.release.style
        audio["tracktotal"] = track['tracktotal']
        audio["discnumber"] = track['disc']
        audio["tracknumber"] = track['number']
        audio["organization"] = release.label
        if searcher is not None:
            audio["lyrics"] = searcher.search_lyrics(track[1])
        else:
            audio["lyrics"] = ''
        if artist.name == release.albumartist:
            audio["albumartist"] = ''
        else:
            audio["albumartist"] = release.album_artist
        audio.save()
