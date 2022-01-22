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

def SolutionCheck(guess, word, t):
    output = ''
    if word == '':
        # Solve with user input
        if t == 0:
            print('\nNot preset: .')
            print('Present: a-z')
            print('Correct: A-Z')
            print('Solved: ENTER')
        print('\n' + str(t+1) + ': ' + guess)
        output = input('>  ')
    else:
        # Solve with known input
        # print(str(t+1) + ': ' + guess)
        if guess == word:
            return ''

        # Get all words that aren't exactly correct
        outTemp = ''
        for i in range(len(guess)):
            if guess[i] == word[i]:
                outTemp += ' '
            else:
                outTemp += word[i]
        
        # Convert to output string 'i..CE'
        for i in range(len(guess)):
            if outTemp[i] != ' ':
                if guess[i] in outTemp:
                    output += guess[i]
                else:
                    output += '.'
            else:
                output += str(guess[i]).upper()
        # print('>  ' + output)
    return output

def Solve(guess, word, previous, excludePos, exclude="", include="", t=0):
    global wordDict

    guessCheck = SolutionCheck(guess, word, t)

    if guessCheck == '':
        if t > 5:
            return False
        return True

    for i in range(len(guess)):
        char = guess[i]
        if guessCheck[i] == '.':
            if char not in exclude:
                exclude += char
        elif guessCheck[i].islower():
            if char not in include:
                include += char

    previous.add(guess)

    regex = ''
    for i in range(len(guess)):
        if guessCheck[i].isupper():
            regex += guess[i]
        else:
            if guess[i] not in excludePos[i]:
                excludePos[i] += guess[i]
            regex += '[^' + "".join(set(exclude + excludePos[i])) + ']'
    # print(regex)
    regex = re.compile(regex)

    # If we don't know any letters get the next starting guess
    # guesses = ['plumb', 'wight', 'seron', 'jacky']
    # if guessCheck.count('.') != len(guessCheck):
    #     guesses = wordDict[len(guess)]
    guesses = wordDict[len(guess)]

    newGuess = ''
    for g in guesses:

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

    return [l[0] for l in sorted(guesses.items(), key=lambda item: item[1], reverse=True)]

def main(guess, word):
    return Solve(guess, word, set(), [""]*len(guess))

if __name__ == "__main__":
    print("> Loading Words")
    # Load common words first so they're searched first
    loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
    formatDictionary()

    # Always start with this guess
    # 96.3% Success
    guess = 'plumb'

    print('[0] Input Word')
    print('[1] Unknown Word')
    t = input('> ')

    if t == '0':
        word = input("Enter 5 Letter Word: ")
        word = word.lower()
        print(main(guess, word))
    else:
        print(main(guess, ''))