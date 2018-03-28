import re
import shutil
import os


class FileRenamer:
    def __init__(self, text):
        self.text = text
        self.processed = self.text

    def reset(self):
        self.processed = self.text

    def replace_tag(self, tag, value):
        if value is None:
            value = ''
        pattern = re.compile(r'\$\{([-_ ]*)' + tag + '([-_ ]*)\}')
        result = re.findall(pattern, self.text)
        if len(result) == 0:
            value = ''
        else:
            prepend = result[0][0]
            append = result[0][1]
        pattern = re.compile(r'(\$\{[-_ ]*' + tag + '[-_ ]*\})')
        result = re.findall(pattern, self.text)
        if len(result) == 0:
            return
        if value == '':
            self.processed = self.processed.replace(result[0], '')
        else:
            self.processed = self.processed.replace(
                result[0], prepend + value + append)

    def rename_file(self, file, track, release, artist):
        extension = file.split('.')[-1]
        self.replace_tag('d', track['disc'])
        self.replace_tag('dt', track['disctotal'])
        self.replace_tag('n', track['number'])
        self.replace_tag('nt', track['tracktotal'])
        self.replace_tag('t', track['title'])
        self.replace_tag('a', artist.name)
        self.replace_tag('b', release.album_artist)
        dirname = os.path.dirname(file)
        if dirname == '':
            dirname = '.' + os.sep
        shutil.move(file, dirname + os.sep + self.processed + '.' + extension)
        self.reset()
