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
    if text.isupper():
        return 'upper'
    if text.istitle():
        return 'title'
    return 'other'


def to_case(text, case):
    if case == 'lower':
        return text.lower()
    if case == 'upper':
        return text.upper()
    if case == 'title':
        return text.title()
    return text
