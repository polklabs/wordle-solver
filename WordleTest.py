import json, re
from multiprocessing import Pool
from sys import exc_info
from Wordle import formatDictionary, getStartGuesses, main, loadDictionary, wordDict
from tqdm import tqdm

loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
formatDictionary()

# plumb

def tryWord(guess):
    size = len(guess)
    failedCount = 0
    for word in wordDict[size]:
    # for word in tqdm(wordDict[size]):
        if main(guess, word) == False:
            failedCount += 1
    errorRate = failedCount/len(wordDict[size])*100
    print(guess + ' - Failed: ' + str(round(errorRate, 2)) + '%')
    return [errorRate, guess]

def CalcUnknownWords(size=5):
    values = []
    with Pool(12) as p:
        values += p.map(tryWord, getStartGuesses(size)[:120])

    print('> Starting Pool 2')
    with Pool(12) as p:
        values += p.map(tryWord, getStartGuesses(size)[-120:])

    values = sorted(values)

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

if __name__ == "__main__":
    # tryWord('about')
    # tryWord('plumb')
    CalcUnknownWords(6)
