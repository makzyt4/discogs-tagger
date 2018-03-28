import argparse


class WordProcessor:
    def __init__(self):
        self.short_words = (
            'for', 'and', 'the', 'of', 'by', 'in', 'at', 'o\'', '\'n\'', 'a',
            'an', '\'n', 'n\'', 'on', 'der', 'die', 'das', 'la', 'el', 'les',
            'as', 'to', 'but'
        )

    def process(self, text):
        if text.lower() == 'untitled':
            return '[untitled]'

        words = text.strip().split(' ')
        for i in range(len(words)):
            if i == 0 or i == len(words) - 1:
                continue
            if words[i].lower() in self.short_words:
                words[i] = words[i].lower()
        return ' '.join(words).strip()
