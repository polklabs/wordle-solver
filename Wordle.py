import re

wordDict = dict()
failCount = 0

def loadDictionary(filename, skip=0):
    global wordDict
    with open(filename, 'r') as f:
        for _ in range(skip):
            f.readline()
        wordList = f.read().splitlines()
        for word in wordList:
            word = word.split()[0].lower()
            wLength = len(word)
            if wLength not in wordDict:
                wordDict[wLength] = dict()
            wordDict[wLength][word] = 1

def formatDictionary():
    global wordDict
    for key in wordDict.keys():
        wordDict[key] = list(wordDict[key])

def Solve(guess, word, previous, exclude="", include="", t=0):
    global wordDict
    # print(str(t+1) + ': ' + guess)

    previous.add(guess)

    if guess == word:
        if t > 5:
            # print(word + '. T=' + str(t+1) + '. Fail')
            return False
        return True

    # Get list of required letters
    # and letters to eclude
    for char in guess:
        if char not in word and char not in exclude:
            exclude += char
        if char in word and char not in include:
            include += char

    regex = ''
    for i in range(len(word)):
        if word[i] == guess[i]:
            regex += word[i]
        else:
            tempInclude = include.replace(guess[i], '')
            if tempInclude == '':
                tempInclude = '.'
            regex += '[^' + exclude + guess[i] + ']'
    # print(regex)
    # print(include)
    regex = re.compile(regex)

    newGuess = ''
    for g in wordDict[len(word)]:

        # Make sure we aren't guessing the same word again
        if g in previous:
            continue

        if bool(re.match(regex, g)) == False:
            continue

        # Make sure all letters in include list are present
        allPresent = True
        for c in include:
            if c not in g:
                allPresent = False
        if allPresent == False:
            continue

        newGuess = g
        break


    if newGuess != '':
        return Solve(newGuess, word, previous, exclude, include, t+1)

    return False

def getStartGuesses(length):
    global wordDict
    # Get the frequest of each letter for
    # words of length X
    letterFreq = dict()
    for w in wordDict[length]:
        for c in w:
            if c not in letterFreq:
                letterFreq[c] = 0
            letterFreq[c] += 1

    # Sort the letters into a list, most common first
    letters = [l[0] for l in sorted(letterFreq.items(), key=lambda item: item[1], reverse=True)]

    # Get the lowest scoring word
    # I.E. Word with the most frequest letters
    guesses = dict()
    for w in wordDict[length]:
        score = 0
        for c in w:
            if w.count(c) > 1:
                break
            score += letters.index(c)
        else:
            guesses[w] = score

    return [l[0] for l in sorted(guesses.items(), key=lambda item: item[1])]

def getStartGuess(length):
    getStartGuesses(length)[-1]

def main(guess, word):
    return Solve(guess, word, set())

if __name__ == "__main__":
    print("> Loading Words")
    # Load common words first so they're searched first
    loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
    formatDictionary()

    word = input("Enter 5 Letter Word: ")
    word = word.lower()
    guess = getStartGuess(len(word))
    print(main(guess, word))