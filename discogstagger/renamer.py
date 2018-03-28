import re


class FileRenamer:
    def __init__(self, text):
        self.text = text
        self.processed = self.text

    def replace_tag(self, tag, value):
        if value is None:
            value = ''
        pattern = re.compile(r'\$\{([-_ ]*)' + tag + '([-_ ]*)\}')
        (prepend, append) = re.findall(pattern, self.text)[0]
        pattern = re.compile(r'(\$\{[-_ ]*' + tag + '[-_ ]*\})')
        result = re.findall(pattern, self.text)[0]
        if value == '':
            self.processed = self.processed.replace(result, '')
            return
        else:
            self.processed = self.processed.replace(
                result, prepend + value + append)
