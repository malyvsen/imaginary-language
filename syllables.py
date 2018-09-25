import re
import random
import numpy as np
from tqdm import trange
from collections import OrderedDict
from Levenshtein import distance
import json
from settings import syllables as settings
import english
import text


syllables = OrderedDict() # {syllable: embedding}


def generate():
    print('Generating syllables...')
    for i in range(settings.num_syllables):
        new_syllable = random_syllable()
        while new_syllable in syllables:
            new_syllable = random_syllable()
        syllables[new_syllable] = np.random.normal(size=english.embedding_dimensions)
    print('Syllables generated')


def save(name='example'):
    file_path = './syllables/' + name + '.json'
    with open(file_path, 'w') as file:
        file.write(json.dumps(syllables))


def load(name='example'):
    global syllables
    file_path = './syllables/' + name + '.json'
    with open(file_path, 'r') as file:
        syllables = json.loads(file.read(), object_pairs_hook=OrderedDict)


def translate_word(english_word):
    if not text.is_word(english_word):
        return english_word
    best_equivalent = english.fuzzy_match(english_word)
    best_equivalent_rank = english.words.index(best_equivalent)
    target_embedding = english.normalized_embeddings[best_equivalent]
    target_num_syllables = settings.min_word_syllables + (settings.max_word_syllables - settings.min_word_syllables) * best_equivalent_rank / len(english.words)
    result = ''
    result_embedding = np.zeros(english.embedding_dimensions)
    for i in range(int(target_num_syllables)):
        best_syllable = max(syllables, key=lambda syllable: english.semantic_similarity(syllables[syllable], target_embedding - result_embedding))
        result += best_syllable
        result_embedding += syllables[best_syllable]
    return result


def translate_text(english_text):
    split = text.split_words(english_text)
    imaginary_words = [text.to_case(translate_word(wordcase[0]), wordcase[1]) for wordcase in tqdm(split)]
    imaginary_text = ''
    for word in imaginary_words:
        if imaginary_text != '' and word[0] not in string.punctuation:
            imaginary_text += ' '
        imaginary_text += word
    return imaginary_text


def random_syllable():
    pattern = random.choice(settings.syllable_patterns)
    result = ''
    for letter in pattern:
        result += random.choice(settings.letter_groups[letter])
    return result


def split_syllables(word, syllable_bank=None):
    if syllable_bank is None:
        syllable_bank = list(syllables)
    pattern = '(' + '|'.join(syllable_bank) + ')'
    return re.findall(pattern, word)


if __name__ == '__main__':
    try:
        generate()
    except KeyboardInterrupt:
        pass
    print() # eat up the left-over loading bar
    print('Name your syllables: ', end='')
    language_name = input()
    save(language_name)
