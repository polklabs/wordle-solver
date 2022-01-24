import json, re
from multiprocessing import Pool
from Wordle import Wordle
from tqdm import tqdm
from FiveLetters import wordDictionary

def tryWord(guess):
    # wordle.loadDictionary(len(guess), 'SUBTLEXus74286wordstextversion.txt', 1, )
    # wordle.formatDictionary()    

    size = len(guess)
    failedCount = 0
    i = 0
    # for word in wordle.wordDict[size]:
    for word in tqdm(wordDictionary):
        wordle = Wordle()
        wordle.wordDict[5] = wordDictionary
        wordle.main(guess, word)
        while wordle.GetNextGuess() != '':
            pass
        if wordle.fail and i < 6779:
            failedCount += 1
        i += 1
    # errorRate = failedCount/len(wordle.wordDict[size])*100
    errorRate = failedCount/6779*100
    print(guess + ' - Failed: ' + str(round(errorRate, 2)) + '%')
    return [errorRate, guess]

def CalcUnknownWords(size=5):
    wordle = Wordle()
    wordle.loadDictionary(size, 'SUBTLEXus74286wordstextversion.txt', 1, )
    wordle.formatDictionary()

    values = []
    print('> Starting Pool 1')
    with Pool(12) as p:
        values += p.map(tryWord, wordle.getStartGuesses(size)[:120])

    print('> Starting Pool 2')
    with Pool(12) as p:
        values += p.map(tryWord, wordle.getStartGuesses(size)[-120:])

    values = sorted(values)

    # List list of words that don't contain any letters from any previous words
    excludeLetters = ''
    results = []
    for i in range(len(values)):
        value = values[i][1]
        ex = excludeLetters
        if ex == '':
            ex = '.'
        regex = '[^' + ex + ']{'+str(size)+'}'
        if bool(re.match(regex, value)) == True:
            results.append(value)
            excludeLetters += "".join(set(value))

    print('Best starting words')
    print(results)

def GenerateDict(filenames, wordSize=5):
    wordle = Wordle()
    for d in filenames:
        wordle.loadDictionary(wordSize, d, 1)
    wordle.formatDictionary()

    with open('FiveLetters.py', 'w') as f:
        f.write('wordDictionary = ' + json.dumps(wordle.wordDict[wordSize], indent=2))

if __name__ == "__main__":
    # tryWord('about')
    # tryWord('plumb')
    # CalcUnknownWords()
    GenerateDict(['SUBTLEXus74286wordstextversion.txt', 'words_alpha.txt'])
