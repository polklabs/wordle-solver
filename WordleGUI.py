from calendar import c
from tkinter import *
from Wordle import Wordle
from FiveLetters import wordDictionary

wordle = Wordle()

win=Tk() #creating the main window and storing the window object in 'win'
win.title('Wordle') #setting title of the window
win.geometry('325x490') #setting the size of the window
win.configure(bg="#121213")

currentRow = 0
row = [] # Buttons in current row
rowState = [] # States of buttons in current row
allButtons = [] # List of all buttons for reset
refreshing = False

def updateState(btnRow, column):
    global currentRow, rowState, row
    if btnRow != currentRow:
        return
    btn = row[column]
    rowState[column] += 1
    rowState[column] = rowState[column] % 3
    if rowState[column] == 0:
        btn['bg'] = "#3a3a3c" # Grey
    if rowState[column] == 1:
        btn['bg'] = "#b59f3b" # Yellow
    if rowState[column] == 2:
        btn['bg'] = "#538d4e" # Green

# Convert rowState to format the Wordle can use
# E.X. P.u..
def getResponse(guess):
    output = ''
    for i in range(len(rowState)):
        state = rowState[i]
        if state == 0:
            output += '.'
        if state == 1:
            output += guess[i]
        if state == 2:
            output += str(guess[i]).upper()
    return output

def addRow(guess):
    global currentRow, row, rowState
    row = []

    # Reset yellow states
    for i in range(len(rowState)):
        if rowState[i] == 1:
            rowState[i] = 0
    
    for i in range(len(guess)):
        btn=Button(win,text=str(guess[i]).upper(), width=2, height=1, pady=0, padx=5, bd=0, font=("Arial bold", 25), bg="#3a3a3c", fg="#d7dadc", command=lambda i=i,currentRow=currentRow:updateState(currentRow, i))
        btn.place(x=16+(i*60),y=20 + (70 * (currentRow)))
        allButtons.append(btn)
        row.append(btn)

        # Set button back to Green state
        if rowState[i] == 2:
            rowState[i]=1
            updateState(currentRow, i)

def nextRow():
    global currentRow, wordle
    if currentRow == 6:
        return
    currentRow += 1
    wordle.guessCheck = getResponse(wordle.guess)
    response = wordle.GetNextGuess()
    if response == '':
        currentRow -= 1

def next(wordle):
    global currentRow
    addRow(wordle.guess)

def reset():
    global wordle, currentRow, allButtons, rowState
    for btn in allButtons:
        btn.destroy()
    allButtons = []
    rowState = [0]*5
    wordle = Wordle()
    wordle.wordDict[5] = wordDictionary
    currentRow = 0
    wordle.main('plumb', '', next)

def refresh():
    wordle._nextGuess()
    for i in range(5):
        row[i]['text'] = str(wordle.guess[i]).upper()

nextBtn=Button(win,text='NEXT', width=6, height=1, bg="#538d4e", fg="#d7dadc", font=("Arial 10"), command=nextRow)
nextBtn.place(x=16,y=450)

refreshBtn=Button(win,text='REFRESH', width=8, height=1, bg="#3a3a3c", fg="#d7dadc", font=("Arial 10"), command=refresh)
refreshBtn.place(x=132,y=450)

resetBtn=Button(win,text='RESET', width=6, height=1, bg="#b59f3b", fg="#d7dadc", font=("Arial 10"), command=reset)
resetBtn.place(x=257,y=450)

reset()

win.mainloop() #running the loop that works as a trigger