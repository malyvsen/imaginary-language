import words
english = None # might be imported later


def high_scores(num_generate=1024, num_display=64):
    word_scores = {}
    for i in range(num_generate):
        word = words.random_word()
        word_scores[word] = words.structural_score(word)

    words_by_score = sorted(word_scores.keys(), key=lambda k: word_scores[k])

    print('High-scoring random words by ascending score:')
    for word in words_by_score[-num_display:]:
        print(word)


def most_frequent(num = 64):
    global english
    import english
    print(f'Most frequent {num} English words:')
    for word in english.words[:num]:
        print(word)


if __name__ == '__main__':
    high_scores()
    print('-' * 32)
    most_frequent()
