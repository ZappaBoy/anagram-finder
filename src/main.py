from anagram_finder import AnagramFinder

if __name__ == '__main__':
    anagram_finder = AnagramFinder()
    result = anagram_finder.find_phrase_anagrams('la pecunia', n_words=3, n_anagrams=100)
    print(result)
