import itertools
import os
from collections import Counter
from string import ascii_lowercase
from typing import List

import pandas
import pandas as pd

dictionaries_dir = os.path.join(os.path.dirname(__file__), 'dictionaries')


class Dictionary:
    def __init__(self, language):
        self._language = language
        self._load_dictionary()

    def _load_dictionary(self):
        self._dictionary_base_dir = os.path.join(dictionaries_dir, self._language)
        self._dictionary_raw_file = os.path.join(self._dictionary_base_dir, 'raw.txt')
        if not os.path.exists(self._dictionary_raw_file):
            raise ValueError('No dictionary found for language ' + self._language)

        self._dictionary_elaborated_file = os.path.join(self._dictionary_base_dir, 'elaborated.csv')

        if not os.path.exists(self._dictionary_elaborated_file):
            self._elaborate_dictionary()
        self._dictionary = pandas.read_csv(self._dictionary_elaborated_file)

    def _elaborate_dictionary(self):
        print('Elaborating dictionary...')
        raw_dictionary = open(self._dictionary_raw_file).read().splitlines()
        elaborated_rows = []
        for word in raw_dictionary:
            word = word.lower()
            letters_occurrences = Counter(letter for letter in word)
            elaborated_row = {'word': word, 'length': len(word)}
            elaborated_row.update({letter: letters_occurrences[letter] for letter in ascii_lowercase})
            elaborated_rows.append(elaborated_row)

        columns = ['word', "length"] + [letter for letter in ascii_lowercase]
        dictionary_df = pd.DataFrame(elaborated_rows, columns=columns)
        dictionary_df.to_csv(self._dictionary_elaborated_file, index=False)

    def print_dictionary_info(self):
        print('Dictionary raw file: ' + self._dictionary_raw_file)
        print('Dictionary elaborated file: ' + self._dictionary_elaborated_file)

    def find_similar_words(self, word: str) -> List[str]:
        letters_occurrences = Counter(letter for letter in word)
        query = 'length=={}'.format(len(word))

        for key, value in letters_occurrences.items():
            query += ' & ' + '{}=={}'.format(key, value)
        results = self._dictionary.query(query)
        return results['word'].to_list()

    @staticmethod
    def _combination_sum(arr, total_sum):
        ans = []
        temp = []
        arr = sorted(list(set(arr)))
        Dictionary._find_numbers(ans, arr, temp, total_sum, 0)
        return ans

    @staticmethod
    def _find_numbers(ans, arr, temp, total_sum, index):
        if total_sum == 0:
            ans.append(list(temp))
            return

        for i in range(index, len(arr)):
            if (total_sum - arr[i]) >= 0:
                temp.append(arr[i])
                Dictionary._find_numbers(ans, arr, temp, total_sum - arr[i], i)
                temp.remove(arr[i])

    @staticmethod
    def _is_valid_anagram(anagram, phrase):
        return sorted(anagram.replace(" ", "")) == sorted(phrase.replace(" ", ""))

    def _get_anagram_in_mask(self, mask, usable_words, original_phrase):
        words_to_combine = []
        for word_length in mask:
            words_to_combine.append(usable_words[word_length])

        anagrams = [' '.join(phrase) for phrase in itertools.product(*words_to_combine) if
                    self._is_valid_anagram(' '.join(phrase), original_phrase)]

        return anagrams

    def find_phrase_anagrams(self, phrase: str, n_words: int, n_anagrams: int = None) -> List[str]:
        original_phrase = phrase
        phrase = phrase.replace(' ', '')
        letters_occurrences = Counter(letter for letter in phrase)
        anagrams = []

        null_columns = list(set(ascii_lowercase).difference(letters_occurrences.keys()))
        query = 'length<={}'.format(len(phrase))
        for letter in null_columns:
            query += ' & ' + '{}==0'.format(letter)
        for letter in letters_occurrences.keys():
            query += ' & ' + '{}<={}'.format(letter, letters_occurrences[letter])
        candidate_words = self._dictionary.query(query)
        words_lengths = Counter(candidate_words.length)
        usable_words = {}
        for word_length in words_lengths:
            fitted_words = candidate_words.loc[candidate_words['length'] == word_length]['word'].to_list()
            usable_words[word_length] = fitted_words

        masks = self._combination_sum(list(words_lengths.keys()), len(phrase))
        masks = [mask for mask in masks if len(mask) <= n_words]
        for mask in masks:
            anagrams_in_mask = self._get_anagram_in_mask(mask, usable_words, original_phrase)
            anagrams.extend(anagrams_in_mask)
            if n_anagrams is not None and len(anagrams) >= n_anagrams:
                return anagrams

        return anagrams
