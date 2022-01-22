import json
from multiprocessing import Pool
from Wordle import Solve, formatDictionary, getStartGuesses, main, loadDictionary, wordDict, getStartGuess
from tqdm import tqdm

loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
formatDictionary()

def tryWord(guess):
    failedCount = 0
    for i in range(len(wordDict[5])):
        word = wordDict[5][i]
        if main(guess, word) == False:
            failedCount += 1
    print(guess + ' - Failed: ' + str(failedCount/len(wordDict[5])*100) + '%')

if __name__ == "__main__":
    with Pool(4) as p:
        p.map(tryWord, getStartGuesses(5)[:10])
