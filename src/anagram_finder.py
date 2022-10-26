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

    def find_similar_words(self, word: str) -> List[str]:
        return self.dictionary.find_similar_words(word)

    def find_word_anagram(self, word: str) -> List[str]:
        similar_words = self.dictionary.find_similar_words(word)
        if len(similar_words) > 0:
            similar_words.remove(word)
        return similar_words

    def find_phrase_anagram(self, phrase: str) -> List[str]:
        phrase = re.sub(r'[^a-zA-Z\s]', '', phrase)
        print(phrase)
        words = phrase.split()
        similar_words = {}
        for word in words:
            similar_words[word] = self.find_similar_words(word)
        return list(similar_words.items())
