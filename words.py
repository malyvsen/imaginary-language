import re
import random
import numpy as np
from settings import words as settings


def random_word():
    length = random.randint(settings.min_word_length, settings.max_word_length + 1)
    return ''.join(random.choice(settings.letters) for i in range(length))


def random_edit(word):
    possible_actions = []
    if len(word) < settings.max_word_length:
        possible_actions.append('add')
    if len(word) > settings.min_word_length:
        possible_actions.append('remove')
    possible_actions.append('change')
    action = random.choice(possible_actions)
    index = np.random.randint(len(word))

    if action == 'add':
        return word[:index] + random.choice(settings.letters) + word[index:]
    if action == 'remove':
        return word[:index] + word[index + 1:]
    if action == 'change':
        return word[:index] + random.choice(settings.letters) + word[index + 1:]


def grouping_score(word, group, epsilon=0):
    '''
    A number in range [0, 1] representing the amount of grouping in a word
    The more grouping, the lower the score
    '''
    groups = re.findall('[' + group + ']+', word)
    group_lengths = np.array([len(x) for x in groups])
    return np.prod((1.0 + epsilon) / (group_lengths + epsilon))


def structural_score(word):
    '''A number in range [0, 1] representing how good a word is structurally'''
    vowel_score = grouping_score(word, settings.vowels, settings.vowel_epsilon)
    consonant_score = grouping_score(word, settings.consonants, settings.consonant_epsilon)
    length_score = 1.0 - (len(word) - settings.min_word_length) / (settings.max_word_length - settings.min_word_length)
    return np.average([vowel_score, consonant_score, length_score],
    weights=[settings.vowel_weight, settings.consonant_weight, settings.length_weight])
