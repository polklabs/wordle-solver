import json
from Wordle import Solve, formatDictionary, getStartGuesses, main, loadDictionary, wordDict, getStartGuess
from tqdm import tqdm

loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
formatDictionary()

# testWords = []
# with open('fail.txt', 'r') as f:
#     testWords = json.loads(f.read())

# guesses = getStartGuesses(5)
# for i in range(len(guesses)):
#     guess = guesses[-(1+i)]
#     failedCount = 0
#     print(guess, end='')
#     for word in testWords:
#         if main(guess, word) == False:
#             failedCount += 1
#     print(': ' + str(failedCount / len(testWords) * 100) + '% ')

# guess = getStartGuess(5)
# guess = 'arose'

for guess in getStartGuesses(5):
    failedCount = 0
    # failed = []
    # for i in tqdm(range(len(wordDict[5]))):
    for i in range(len(wordDict[5])):
        word = wordDict[5][i]
        if main(guess, word) == False:
            failedCount += 1
            # failed.append(word)
    print(guess + ' - Failed: ' + str(int(failedCount/len(wordDict[5])*100)) + '%')
# with open('fail.txt', 'w') as f:
#     f.write(json.dumps(failed, indent=2))