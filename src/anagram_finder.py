import re
from typing import List

from dictionary import Dictionary

default_language = 'it'


class AnagramFinder:
    language = default_language

    def __init__(self, language=default_language):
        self.set_language(language)

    def set_language(self, language):
        self.language = language
        self._load_dictionary()

    def _load_dictionary(self):
        self.dictionary = Dictionary(self.language)

    @staticmethod
    def _preprocess(phrase: str) -> str:
        phrase = re.sub(r'[^a-zA-Z\s]', '', phrase)
        return phrase.lower()

    def find_similar_words(self, word: str) -> List[str]:
        return self.dictionary.find_similar_words(word)

    def find_word_anagram(self, word: str) -> List[str]:
        similar_words = self.dictionary.find_similar_words(word)
        if len(similar_words) > 0:
            similar_words.remove(word)
        return similar_words

    def find_words_anagram(self, phrase: str) -> dict:
        phrase = self._preprocess(phrase)
        words = phrase.split()
        similar_words = {}
        for word in words:
            similar_words[word] = self.find_similar_words(word)
        return similar_words

    def find_phrase_anagrams(self, phrase: str, n_words: int = None, n_anagrams=None) -> List[str]:
        if n_words is None:
            n_words = len(phrase.replace(' ', ''))
        phrase = self._preprocess(phrase)
        anagrams = self.dictionary.find_phrase_anagrams(phrase, n_words=n_words, n_anagrams=n_anagrams)

        return anagrams
