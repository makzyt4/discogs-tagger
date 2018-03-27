import os


class SettingsManager:
    def __init__(self, filename=os.path.expanduser('~') + os.sep + 'discogs-tagger.settings'):
        self.filename = filename
        self.default_settings = {
            'format': '${discd}${tracknum} - ${title}',
            'artist-query-size': 5,
            'tag-lyrics': 'false'
        }

    def load(self):
        self.settings = self.default_settings
        try:
            with open(self.filename) as f:
                content = [x.strip() for x in f.readlines()]
                for line in content:
                    key = line.split('=')[0]
                    val = line.split('=')[1]
                self.settings[key] = val
                return True
        except FileNotFoundError:
            return False

    def generate(self):
        with open(self.filename, 'w') as f:
            for k, v in self.default_settings.items():
                f.write("{}={}\n".format(k, v))
        return self.default_settings
