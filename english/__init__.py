from Levenshtein import distance
from collections import OrderedDict
import numpy as np
from tqdm import tqdm


def load_glove(file_path='./english/glove.6B.300d.txt'):
    print('Loading GloVe embeddings...')
    f = open(file_path, 'r')
    model = OrderedDict()
    for line in tqdm(f):
        split_line = line.split()
        word = split_line[0]
        embedding = np.array([float(val) for val in split_line[1:]])
        model[word] = embedding
    return model


embeddings = load_glove()

normalized_embeddings = OrderedDict()
for word in embeddings:
    normalized_embeddings[word] = embeddings[word] / np.linalg.norm(embeddings[word])
words = list(embeddings)

embedding_dimensions = len(embeddings[words[0]])

frequency_distribution = [1 / (i + 1) for i in range(len(words))] # Zipf's law
frequency_distribution /= np.sum(frequency_distribution)
word_frequencies = OrderedDict()
for i in range(len(words)):
    word_frequencies[words[i]] = frequency_distribution[i]


def fuzzy_match(word):
    '''The most similar-looking word that has been loaded (possibly the same word)'''
    if word in words:
        return word
    return min(words, key=lambda test: distance(word, test))


def semantic_similarity(a, b):
    '''A number between 0 and 1 representing how similar the meanings of two words are'''
    a_vec = normalized_embeddings[a] if type(a) is str else (a / np.linalg.norm(a) if np.linalg.norm(a) > 0 else a)
    b_vec = normalized_embeddings[b] if type(b) is str else (b / np.linalg.norm(b) if np.linalg.norm(b) > 0 else b)
    return (np.dot(a_vec, b_vec) + 1) / 2


def neighborhood(english_word, num, wordbank=None):
    '''A list of at most the num nearest English words in embedding space'''
    if wordbank == None:
        wordbank = words
    words_sorted = sorted(wordbank, key=lambda word: semantic_similarity(english_word, word))
    if len(words_sorted) > num:
        return words_sorted[-num:]
    return words_sorted


def euclidean_distance(a, b):
    '''Another measure of difference between two words - non-normalized'''
    a_vec = normalized_embeddings[a] if type(a) is str else a
    b_vec = normalized_embeddings[b] if type(b) is str else b
    return np.linalg.norm(a_vec - b_vec)
