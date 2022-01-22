import json
from multiprocessing import Pool
from Wordle import formatDictionary, getStartGuesses, main, loadDictionary, wordDict
from tqdm import tqdm

loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
formatDictionary()

# plumb

def tryWord(guess):
    failedCount = 0
    for word in wordDict[5]:
    # for word in tqdm(wordDict[5]):
        if main(guess, word) == False:
            failedCount += 1
    errorRate = failedCount/len(wordDict[5])*100
    print(guess + ' - Failed: ' + str(round(errorRate, 2)) + '%')
    return [errorRate, guess]

if __name__ == "__main__":
    # tryWord('about')
    # tryWord('plumb')
    with Pool(12) as p:
        out = p.map(tryWord, getStartGuesses(5)[-120:])
        
        with open('results2.json', 'w') as f:
            f.write(json.dumps(out, indent=2))
