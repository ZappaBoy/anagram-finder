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
        dictionary_df.to_csv(self._dictionary_elaborated_file)

    def print_dictionary_info(self):
        print('Dictionary raw file: ' + self._dictionary_raw_file)
        print('Dictionary elaborated file: ' + self._dictionary_elaborated_file)

    def find_similar_words(self, word: str) -> List[str]:
        word = word.lower()
        letters_occurrences = Counter(letter for letter in word)
        query = 'length=={}'.format(len(word))

        for key, value in letters_occurrences.items():
            query += ' & ' + '{}=={}'.format(key, value)
        results = self._dictionary.query(query)
        return results['word'].to_list()
