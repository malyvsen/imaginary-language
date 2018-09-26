class words:
    min_word_length = 2
    max_word_length = 16
    vowels = 'aeiouy'
    consonants = 'bcdfghjklmnpqrstvwxz'
    letters = vowels + consonants

    # tolerance to sequences containing only vowels/consonants
    vowel_epsilon = 0
    consonant_epsilon = 2

    # what matters how much when a word's structural score is evaluated
    vowel_weight = 4
    consonant_weight = 6
    length_weight = 1


class syllables:
    num_syllables = 512
    syllable_patterns = ['ba', 'bja', 'bjah', 'bah', 'qa', 'ja', 'qaj', 'jaj', 'ha', 'haj']
    letter_groups = {'a': 'aeiouy', 'b': 'bcdfgkpstvxz', 'j': 'jlr', 'h': 'hmn', 'q': 'qw'}
    min_word_syllables = 1
    max_word_syllables = 32


class dictionary:
    num_words = 2 ** 16

    max_distance = 16 # the higher, the more the language spreads over the word space
    distance_power = 1 # the higher, the more words which are already considered similar are 'pulled together'

    # how important it is for the language to be good when it comes to...
    semantic_weight = 2
    structure_weight = 1

    num_alternatives = 1024 # how many alternatives we consider for each word - an epoch count of sorts
    num_neighbors = 32 # how many similar words we look at when calculating semantic score
    num_random_comparisons = 32 # how many other, randomly selected words we also look at
