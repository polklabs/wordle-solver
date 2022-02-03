import json
from Wordle import Wordle

def GenerateDict(filenames, wordSize=5):
    wordle = Wordle()
    for d in filenames:
        wordle.loadDictionary(wordSize, d, 1)
    wordle.formatDictionary()

    with open('FiveLetters.py', 'w') as f:
        f.write('wordDictionary = ' + json.dumps(wordle.wordDict[wordSize], indent=2))

if __name__ == "__main__":
    GenerateDict(['SUBTLEXus74286wordstextversion.txt', 'words_alpha.txt'])