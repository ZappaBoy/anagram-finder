from anagram_finder import AnagramFinder

if __name__ == '__main__':
    anagram_finder = AnagramFinder()
    result = anagram_finder.find_phrase_anagrams('la pecunia')
    print(result)
