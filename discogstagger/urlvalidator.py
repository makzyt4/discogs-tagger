import re


class URLValidator:
    def _validate_uri(self, text):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, text)

    def validate(self, text):
        if type(text) != str:
            return False
        if not self._validate_uri(text):
            return False
        regex = re.compile('^https?://(www.)?discogs.com/[\S]+/release/\d+$',
                           re.IGNORECASE)
        return re.match(regex, text)
