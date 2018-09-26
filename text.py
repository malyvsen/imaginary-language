import re
import string


def split_words(text):
    '''Split text into lowercase words (or parts of words that will fit the embeddings), paired with original cases'''
    words = re.findall('([a-zA-Z]+|[0-9a-zA-Z]+|[a-zA-Z0-9' + string.punctuation + ']+)', text)
    return [(word.lower(), case(word)) for word in words]


def is_word(text):
    if len(re.findall('[0-9]+', text)) > 0:
        return False
    if len(re.findall('[a-zA-Z]+', text)) == 0:
        return False
    return True


def case(text):
    if text.islower():
        return 'lower'
    if text.istitle():
        return 'title'
    if text.isupper():
        return 'upper'
    return 'other'


def to_case(text, case):
    if case == 'lower':
        return text.lower()
    if case == 'title':
        return text.title()
    if case == 'upper':
        return text.upper()
    return text


def ending_distance(a, b):
    '''A measure of how different two strings are'''
    for i in range(min(len(a), len(b))):
        if a[:i+1] != b[:i+1]:
            return max(len(a), len(b)) - i
    return abs(len(a) - len(b))
