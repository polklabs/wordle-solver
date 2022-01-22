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

def Solve(guess, word, previous, excludePos, exclude="", include="", t=0):
    global wordDict
    # print(str(t+1) + ': ' + guess)

    previous.add(guess)

    if guess == word:
        if t > 5:
            return False
        return True

    # Get list of required letters
    # and letters to exclude
    for char in guess:
        if char not in word:
            if char not in exclude:
                exclude += char
        else:
            if char not in include:
                include += char

    regex = ''
    for i in range(len(guess)):
        if word[i] == guess[i]:
            regex += word[i]
        else:
            if guess[i] not in excludePos[i]:
                excludePos[i] += guess[i]
            regex += '[^' + "".join(set(exclude + excludePos[i])) + ']'
    # print(regex)
    regex = re.compile(regex)

    newGuess = ''
    for g in wordDict[len(word)]:

        # Make sure we aren't guessing the same word again
        # Prevent infinite loops
        if g in previous:
            continue

        # Filter guesses based on excluded letters
        if bool(re.match(regex, g)) == False:
            continue

        # Make sure all letters in include list are present
        allPresent = True
        for c in include:
            if c not in g:
                allPresent = False
                break
        if allPresent == False:
            continue

        newGuess = g
        break

    if newGuess != '':
        return Solve(newGuess, word, previous, excludePos, exclude, include, t+1)

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

    return [l[0] for l in sorted(guesses.items(), key=lambda item: item[1], reverse=False)]

def getStartGuess(length):
    getStartGuesses(length)[-1]

def main(guess, word):
    return Solve(guess, word, set(), [""]*len(word))

if __name__ == "__main__":
    print("> Loading Words")
    # Load common words first so they're searched first
    loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
    formatDictionary()

    word = input("Enter 5 Letter Word: ")
    word = word.lower()
    guess = getStartGuess(len(word))
    print(main(guess, word))