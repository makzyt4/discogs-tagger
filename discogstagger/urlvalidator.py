import re
import urlparse

class UrlValidator:
    def _validate_uri(text):
        try:
            result = urlparse(x)
            return result.scheme and result.netloc and result.path
        except:
            return False

    def validate_url(text):
        if not _validate_uri(text):
            return False
        regex = re.compile('^https?://(www.)?discogs.com/[\S]+/release/\d+$',
                   re.IGNORECASE)
        return re.match(regex, text)
