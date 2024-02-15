# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:52:21 2024

@author: 
"""

import string

word_length = 5;                              # wordle words are 5 characters long
word_file_location = "./answers.txt"          # location of list of possible answer words
exclude_ends_with_s = True                    # wordle answers are never plural
vowels_are_worthless = True                   # assign zero score to vowels?
exclude_words_with_duplicate_letters = True   # exclude from results list words with multiple of the same letter?
found_in_place_weight = 1.0                   # in scoring words, score weight for letters found in-place

vowels = ['a','e','i','o','u','y']

letter_weights = {'a' : 1.0,
                  'b' : 1.0,
                  'c' : 1.0,
                  'd' : 1.0,
                  'e' : 1.0,
                  'f' : 1.0,
                  'g' : 1.0,
                  'h' : 1.0,
                  'i' : 1.0,
                  'j' : 1.0,
                  'k' : 1.0,
                  'l' : 1.0,
                  'm' : 1.0,
                  'n' : 1.0,
                  'o' : 1.0,
                  'p' : 1.0,
                  'q' : 1.0,
                  'r' : 1.0,
                  's' : 1.0,
                  't' : 1.0,
                  'u' : 1.0,
                  'v' : 1.0,
                  'w' : 1.0,
                  'x' : 1.0,
                  'y' : 1.0,
                  'z' : 1.0}

banned_characters = [".", ",", "-", "'", " ", r'/', '3']


def valid_words_of_length():
    out = []
    with open(word_file_location) as word_file:
        for _word in word_file:
            _word = _word.strip()
            valid = True;
            if exclude_ends_with_s and _word.endswith('s'):
                valid = False
            if len(_word) != word_length:
                valid = False
            for _banned_char in banned_characters:
                if _banned_char in _word:
                    valid = False
                    break
            if valid:
                out.append(_word.lower())
    return out


def letter_values(word_list):
    out = {}
    for _letter in string.ascii_lowercase:
        out[_letter] = 0
        
    for _word in word_list:
        for _character in _word:
            if vowels_are_worthless:
                if _character in vowels:
                    continue
            out[_character] += 1 * letter_weights[_character]
    return out


def has_duplicate_letters(word):
    for _char in word:
        count = 0
        for __char in word:
            if _char == __char:
                count += 1
                if count > 1:
                    return True
    return False


def word_scores(list_words, dict_letter_values):
    out = {}
    for word in list_words:
        if exclude_words_with_duplicate_letters and has_duplicate_letters(word):
            continue
        word_score = 0
        charpos1 = 0
        for char in word:  
            charpos1 += 1
            for _word in list_words:
                charpos2 = 0
                for _char in _word:
                    charpos2 += 1
                    if char == _char:
                        if (vowels_are_worthless and (char in vowels)) == False:
                            if charpos1 == charpos2:
                                word_score += 1 * letter_weights[char] * found_in_place_weight
                            else:
                                word_score += 1 * letter_weights[char]
        out[word] = word_score
    return out


def sorted_scored_words(dict_word_scores):
    return sorted(dict_word_scores.items(), key=lambda kv: kv[1], reverse = True)


                    
if __name__ == "__main__":
    words = valid_words_of_length()
    dict_letter_values = letter_values(words)
    dict_word_scores = word_scores(words, dict_letter_values)
    results = sorted_scored_words(dict_word_scores)
    print(results[0:10])
        