# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:52:21 2024

@author: Nick Oleska and the hon. Rev. Jason Manz
TODO: get rank of a word
      incorporate allowed guess words. currently works off of answers only 
"""

import string

WORD_LENGTH = 5                               # wordle words are 5 characters long
WORD_FILE_LOCATION = "./answers.txt"          # location of list of possible answer words
EXCLUDE_ENDS_WITH_S = True                    # wordle answers are never plural
VOWELS_ARE_WORTHLESS = True                   # assign zero score to vowels?
EXCLUDE_WORDS_WITH_DUPLICATE_LETTERS = True   # exclude from results list words with multiple of the same letter?
FOUND_IN_PLACE_WEIGHT = 10.0                   # in scoring words, score weight for letters found in-place

vowels = ['a', 'e', 'i', 'o', 'u', 'y','s','l','a','n','t']

letter_weights = {'a': 1.0,
                  'b': 1.0,
                  'c': 1.0,
                  'd': 1.0,
                  'e': 1.0,
                  'f': 1.0,
                  'g': 1.0,
                  'h': 1.0,
                  'i': 1.0,
                  'j': 1.0,
                  'k': 1.0,
                  'l': 1.0,
                  'm': 1.0,
                  'n': 1.0,
                  'o': 1.0,
                  'p': 1.0,
                  'q': 1.0,
                  'r': 1.0,
                  's': 1.0,
                  't': 1.0,
                  'u': 1.0,
                  'v': 1.0,
                  'w': 1.0,
                  'x': 1.0,
                  'y': 1.0,
                  'z': 1.0}

banned_characters = [".", ",", "-", "'", " ", r'/', '3']


def valid_words():
    '''
    Processes and checks words in word-per-line text document
    for compliance with Wordle and configuration variables.

    Returns
    -------
    out : LIST
        List of lowercase alpha-only 'valid' words.

    '''
    out = []
    with open(WORD_FILE_LOCATION) as word_file:
        for _word in word_file:
            _word = _word.strip().lower()
            valid = True
            if EXCLUDE_ENDS_WITH_S and _word.endswith('s'):
                valid = False
            if len(_word) != WORD_LENGTH:
                valid = False
            for _banned_char in banned_characters:
                if _banned_char in _word:
                    valid = False
                    break
            if valid:
                out.append(_word)
    return out


def letter_values(word_list):
    '''
    Creates dictionary of numeric scores for alphabet letters.
    Score is based on how many times the letter appears in the 
    word list.

    Parameters
    ----------
    word_list : LIST
        List of individual lowercase words.

    Returns
    -------
    out : DICTIONARY
        Keys: Individual lowercase words.
        Values: Numeric scores of those words

    '''
    out = {}
    for _letter in string.ascii_lowercase:
        out[_letter] = 0
    for _word in word_list:
        for _character in _word:
            if VOWELS_ARE_WORTHLESS:
                if _character in vowels:
                    continue
            out[_character] += 1 * letter_weights[_character]
    return out


def has_duplicate_letters(word):
    '''
    Returns true if a word contains more than one instance of any letter.

    Parameters
    ----------
    word : STRING
        A single word.

    Returns
    -------
    bool
        True if there is any letter that appears more than once in the input 
        string.
        False otherwise.

    '''
    for _char in word:
        count = 0
        for __char in word:
            if _char == __char:
                count += 1
                if count > 1:
                    return True
    return False


def word_scores(list_words):
    '''
    Generates dictionary of word scores. Words' scores are based on prevalence
    of their letters in the input list, as well as configuration options and
    weights.

    Parameters
    ----------
    list_words : LIST
        List of individual lowercase words.

    Returns
    -------
    out : DICTIONARY
        Keys: individual lowercase words.
        Values: score numbers.

    '''
    out = {}
    for word in list_words:
        if EXCLUDE_WORDS_WITH_DUPLICATE_LETTERS and has_duplicate_letters(word):
            continue
        word_score = 0
        character_index_1 = 0
        for char in word:
            character_index_1 += 1
            for _word in list_words:
                character_index_2 = 0
                for _char in _word:
                    character_index_2 += 1
                    if char == _char:
                        if (VOWELS_ARE_WORTHLESS and (char in vowels)) == False:
                            if character_index_1 == character_index_2:
                                word_score += 1 * letter_weights[char] * FOUND_IN_PLACE_WEIGHT
                            else:
                                word_score += 1 * letter_weights[char]
        out[word] = word_score
    return out


def sorted_scored_words(dict_x):
    '''
    Sorts input dict by VALUEs, descending.

    Parameters
    ----------
    dict_word_scores : DICTIONARY
        Keys: individual lowercase words
        Values: numeric word scores

    Returns
    -------
    DICTIONARY
        Sorted by values, in descending order.
        Keys: individual lowercase words.
        Values: numeric word scores

    '''
    return sorted(dict_x.items(), key=lambda kv: kv[1], reverse=True)


if __name__ == "__main__":
    words = valid_words()
    #dict_letter_values = letter_values(words)
    dict_word_scores = word_scores(words)
    results = sorted_scored_words(dict_word_scores)
    for i in range(0, 10):
        print(results[i])
