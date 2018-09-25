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
        syllables[new_syllable] = np.random.normal(scale=settings.syllable_vector_scale, size=english.embedding_dimensions)
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
    target_distance = settings.distance_epsilon * settings.base_distance / (english.words.index(best_equivalent) + settings.distance_epsilon)
    result = ''
    result_embedding = np.zeros(english.embedding_dimensions)
    for used_syllables in range(settings.max_word_syllables):
        best_syllable = min(syllables, key=lambda syllable: english.euclidean_distance(result_embedding + syllables[syllable], best_equivalent))
        if english.euclidean_distance(result_embedding + syllables[best_syllable], best_equivalent) > english.euclidean_distance(result_embedding, best_equivalent):
            break # FIXME: this happens (statistically) always... because high-dimensional space?
        result += best_syllable
        result_embedding += syllables[best_syllable]
        if english.euclidean_distance(result_embedding, best_equivalent) < target_distance:
            break
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
