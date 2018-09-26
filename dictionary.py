import string
import re
import json
import random
import numpy as np
from collections import OrderedDict
from tqdm import tqdm, trange
import text
import words
import english
from settings import dictionary as settings


dictionary = OrderedDict() # an English-Imaginary dictionary


def generate():
    '''Create translations for num_words most frequent English words'''
    print('Generating dictionary...')
    for english_word in tqdm(english.words[:settings.num_words]):
        if english_word in dictionary:
            continue
        if not text.is_word(english_word):
            dictionary[english_word] = english_word
            continue
        compare_to = comparison_sample(english_word)
        dictionary[english_word] = words.random_word()
        score = translation_score(english_word, dictionary[english_word], compare_to)
        for i in trange(settings.num_alternatives):
            candidate = words.random_edit(dictionary[english_word])
            candidate_score = translation_score(english_word, candidate, compare_to)
            if candidate in dictionary:
                continue
            if candidate_score > score:
                dictionary[english_word] = candidate
                score = candidate_score


def save(name='example'):
    file_path = './dictionaries/' + name + '.json'
    with open(file_path, 'w') as file:
        file.write(json.dumps(dictionary))


def load(name='example'):
    global dictionary
    file_path = './dictionaries/' + name + '.json'
    with open(file_path, 'r') as file:
        dictionary = json.loads(file.read(), object_pairs_hook=OrderedDict)


def translate_word(english_word):
    if not text.is_word(english_word):
        return english_word
    best_equivalent = english.fuzzy_match(english_word)
    if best_equivalent not in dictionary:
        best_equivalent = max(dictionary, key=lambda word: english.semantic_similarity(best_equivalent, word))
    return dictionary[best_equivalent]


def translate_text(english_text):
    split = text.split_words(english_text)
    imaginary_words = [text.to_case(translate_word(wordcase[0]), wordcase[1]) for wordcase in tqdm(split)]
    imaginary_text = ''
    for word in imaginary_words:
        if imaginary_text != '' and word[0] not in string.punctuation:
            imaginary_text += ' '
        imaginary_text += word
    return imaginary_text


def translation_score(english_word, imaginary_word, compare_to):
    '''
    A number in range [0, 1] representing how good a given english-imaginary translation is
    Takes into account:
        -the target edit distance from words in compare_to
        -the structural score of the word
    '''
    semantic_loss = 0
    total_similarity = 0
    for word in compare_to:
        current_similarity = english.semantic_similarity(english_word, word)
        current_loss = target_distance(current_similarity) - text.ending_distance(imaginary_word, dictionary[word])
        current_loss = np.abs(current_loss) * current_similarity # we care more about neighborhood structure
        semantic_loss += current_loss
        total_similarity += current_similarity
    if total_similarity > 0:
        semantic_loss /= total_similarity
    semantic_loss /= settings.max_distance
    semantic_score = 1 - semantic_loss
    return np.average([semantic_score, words.structural_score(imaginary_word)],
    weights=[settings.semantic_weight, settings.structure_weight])


def target_distance(similarity):
    '''The target edit distance between two words of given semantic similarity'''
    return (1 - similarity) ** settings.distance_power * settings.max_distance


def comparison_sample(english_word):
    '''A list of English words to compare the given word to'''
    words_sorted = sorted(dictionary, key=lambda word: english.semantic_similarity(english_word, word))
    result = []
    if len(words_sorted) > 0:
        result = [random.choice(words_sorted) for i in range(settings.num_random_comparisons)]
    if len(words_sorted) > settings.num_neighbors:
        result += words_sorted[-settings.num_neighbors:]
    else:
        result += words_sorted
    return result


if __name__ == '__main__':
    try:
        generate()
    except KeyboardInterrupt:
        pass
    print() # eat up the left-over loading bar
    print('Name your dictionary: ', end='')
    language_name = input()
    save(language_name)
