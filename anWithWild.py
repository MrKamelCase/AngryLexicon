#! /usr/bin/env python3

import sys

DEFAULT_DICTIONARY = "/usr/share/dict/words"


def getAnagrams(rackStr, dictFileName=DEFAULT_DICTIONARY):
    """Find anagrams of rackStr in dictFileName, allowing * for wildcard"""
    wordsFileName = dictFileName
    rack = list(rackStr)
    solutions = dict()
    with open(wordsFileName) as words:
        for word in words:
            word = word.strip().lower()
            if len(word) < 2:
                continue
            testRack = rack.copy()
            spelled = ""
            used = ""
            for char in word:
                if char in testRack:
                    testRack.remove(char)
                    spelled += char
                    used += char
                elif "*" in testRack:
                    testRack.remove("*")
                    spelled += char
                    used += "*"
                else:
                    spelled = ""
                    break
                if len(spelled) == len(word):
                    solutions[spelled] = used
    return solutions


def main(rack, dictionary):
    return getAnagrams(rack, dictionary)


if __name__ == "__main__":
    rack = sys.argv[1]
    try:
        dictionary = sys.argv[2]
    except IndexError:
        dictionary = "/home/kthing/Documents/Projects/Scrabble/WWFWords.txt"
    print(main(rack, dictionary))
