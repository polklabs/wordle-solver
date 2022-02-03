import json, re
from multiprocessing import Pool
from itertools import repeat
from Wordle import Wordle
from tqdm import tqdm
from FiveLetters import wordDictionary

def guess(guess, initialGuesses, words):
    skip = False
    for letter in guess:
        for g in initialGuesses:
            if letter in g:
                skip = True
    if skip == True:
        return [1, 7, guess]
    
    t = 0
    fails = 0
    for word in words:
        wordle = Wordle()
        wordle.wordDict[5] = wordDictionary
        wordle.initialGuesses = initialGuesses + [guess]
        wordle.main('', word)
        while wordle.GetNextGuess() != '':
            pass
        if wordle.fail:
            fails += 1
        t += wordle.t

    avgT = t/len(words)
    failPer = fails/len(words)
    print(guess + ' -> T: ' + str(round(avgT, 2)) + ', Fail: ' + str(round(failPer*100, 2)) + '%')
    return [failPer, avgT, guess]

def TestWords(initialGuesses = []):
    words = []
    with open('testWords.json', 'r') as f:
        words = json.loads(f.read())

    values = []
    with Pool(12) as p:
        # values += p.map(guess, wordDictionary[:6778])
        values += p.starmap(guess, zip(wordDictionary[:677], repeat(initialGuesses), repeat(words)))
        # values += p.map(lambda p: guess(p, initialGuesses, words), wordDictionary[:677])

    values = sorted(values, key=1)
    values = sorted(values, key=0)

    print(values[:10])

if __name__ == "__main__":
    TestWords()
