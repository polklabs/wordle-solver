import re
from FiveLetters import wordDictionary

class Wordle:
    def __init__(self):
        self.wordDict = dict()
        self.guess = ''
        self.word = ''
        self.t = 0
        self.previous = set()
        self.excludePos = []
        self.exclude = ""
        self.include = ""
        self.fail = False
        self.initialGuesses = ['plumb', 'wight', 'seron', 'jacky']
        self.guesses = []
        self.guessRegex = ''
        self.guessIndex = 0

    def loadDictionary(self, wordSize, filename, skip=0):
        with open(filename, 'r') as f:
            for _ in range(skip):
                f.readline()
            wordList = f.read().splitlines()
            for word in wordList:
                word = word.split()[0].lower()
                wLength = len(word)
                if wLength == wordSize:
                    if wLength not in self.wordDict:
                        self.wordDict[wLength] = dict()
                    self.wordDict[wLength][word] = 1

    def formatDictionary(self):
        for key in self.wordDict.keys():
            self.wordDict[key] = list(self.wordDict[key])

    def SolutionCheck(wordle):
        output = ''
        if wordle.word == '':
            # Solve with user input
            if wordle.t == 0:
                print('\nNot preset: "."')
                print('Present: "a-z"')
                print('Correct: "A-Z"')
                print('Not a valid word: "?"')
                print('Solved: ENTER')
            print('\n' + str(wordle.t+1) + ': ' + wordle.guess)
            output = input('>  ')
        else:
            # Solve with known input
            # print(str(t+1) + ': ' + guess)
            if wordle.guess == wordle.word:
                wordle.guessCheck = output
                return

            # Get all words that aren't exactly correct
            outTemp = ''
            for i in range(len(wordle.guess)):
                if wordle.guess[i] == wordle.word[i]:
                    outTemp += ' '
                else:
                    outTemp += wordle.word[i]
            
            # Convert to output string 'i..CE'
            for i in range(len(wordle.guess)):
                if outTemp[i] != ' ':
                    if wordle.guess[i] in outTemp:
                        output += wordle.guess[i]
                    else:
                        output += '.'
                else:
                    output += str(wordle.guess[i]).upper()
            # print('>  ' + output)
        wordle.guessCheck = output

    def _nextGuess(self):
        for i in range(self.guessIndex, len(self.guesses)):
            self.guessIndex = i
            g = self.guesses[i]

            # Make sure we aren't guessing the same word again
            # Prevent infinite loops
            if g in self.previous:
                continue

            # Filter guesses based on excluded letters
            if bool(re.match(self.guessRegex, g)) == False:
                continue

            # Make sure all letters in include list are present
            allPresent = True
            for c in self.include:
                if c not in g:
                    allPresent = False
                    break
            if allPresent == False:
                continue

            self.guess = g
            self.guessIndex = i+1
            return g
        return ''

    def GetNextGuess(self):
        if self.guessCheck == '':
            if self.t > 5:
                self.fail = True
                # print(self.word)
            return ''

        for i in range(len(self.guess)):
            char = self.guess[i]
            if self.guessCheck[i] == '.':
                if char not in self.exclude and char not in self.guessCheck:
                    self.exclude += char
            elif self.guessCheck[i].islower():
                if char not in self.include:
                    self.include += char

        self.previous.add(self.guess)

        self.guessRegex = ''
        for i in range(len(self.guess)):
            if self.guessCheck[i].isupper():
                self.guessRegex += self.guess[i]
            else:
                if self.guess[i] not in self.excludePos[i]:
                    self.excludePos[i] += self.guess[i]
                self.guessRegex += '[^' + "".join(set(self.exclude + self.excludePos[i])) + ']'
        
        # print(regex)
        # print(self.include)
        # print(self.previous)

        self.guessRegex = re.compile(self.guessRegex)
        self.guesses = self.initialGuesses
        # If we don't know any letters get the next starting guess
        if self.guessCheck.count('.') != len(self.guessCheck) or len(self.guesses) == 0:
            self.guesses = self.wordDict[len(self.guess)]

        self.guessIndex = 0
        out = self._nextGuess()
        self.t += 1
        self.callback(self)

        while self.guessCheck == '?':
            out = self._nextGuess()
            self.callback(self)

        return out

    def getStartGuesses(self, length, reversed=True):
        global wordDict
        # Get the frequest of each letter for
        # words of length X
        letterFreq = dict()
        for w in self.wordDict[length]:
            for c in w:
                if c not in letterFreq:
                    letterFreq[c] = 0
                letterFreq[c] += 1

        # Sort the letters into a list, most common first
        letters = [l[0] for l in sorted(letterFreq.items(), key=lambda item: item[1], reverse=True)]

        # Score all the words based on the frequecy of their letters
        guesses = dict()
        for w in self.wordDict[length]:
            score = 0
            for c in w:
                if w.count(c) > 1:
                    break
                score += letters.index(c)
            else:
                guesses[w] = score

        return [l[0] for l in sorted(guesses.items(), key=lambda item: item[1], reverse=reversed)]

    def main(self, guess="", word="", callback=SolutionCheck):
        if guess == '':
            # Always start with 'plumb'
            # 96.3% Success rate
            self.guess = self.initialGuesses[0]
        else:
            self.guess = guess
        self.callback = callback
        self.word = word
        self.callback(self)
        self.excludePos = [""]*len(self.guess)

if __name__ == "__main__":

    wordle = Wordle()

    # To solve a 5 letter word
    # Load from py file to include in executable
    wordle.wordDict[5] = wordDictionary

    # To solve a non 5 letter word
    # wordLength = 6
    # wordle.loadDictionary(wordLength, 'SUBTLEXus74286wordstextversion.txt', 1)
    # wordle.formatDictionary()
    # wordle.initialGuesses = [wordle.getStartGuesses(wordLength)[0]]

    word = input("Enter 5 Letter Word or ENTER for unknown: ")
    word = word.lower()
    wordle.main("", word)
    while wordle.GetNextGuess() != '':
        pass
    print('Fail:' + str(wordle.fail))