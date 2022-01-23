from tkinter import *
from Wordle import Wordle

wordle = Wordle()

win=Tk() #creating the main window and storing the window object in 'win'
win.title('Wordle') #setting title of the window
win.geometry('325x416') #setting the size of the window
win.configure(bg="#121213")

currentRow = 0
row = []
rowState = []
allButtons = []

def func(btnRow, column):#function of the button
    global currentRow, rowState, row
    if btnRow != currentRow:
        return
    rowState[column] += 1
    rowState[column] = rowState[column] % 3
    if rowState[column] == 0:
        row[column]['bg'] = "#3a3a3c"
    if rowState[column] == 1:
        row[column]['bg'] = "#b59f3b"
    if rowState[column] == 2:
        row[column]['bg'] = "#538d4e"

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
    rowState = []
    for i in range(len(guess)):
        char = guess[i]
        btn=Button(win,text=str(char).upper(), width=2, height=1, pady=0, padx=5, bd=0, font=("Arial bold", 25), bg="#3a3a3c", fg="#d7dadc", command=lambda i=i:func(currentRow, i))
        btn.place(x=16+(i*60),y=20 + (70 * (currentRow)))
        allButtons.append(btn)
        row.append(btn)
        rowState.append(0)

def nextRow():
    global currentRow, wordle
    if currentRow == 6:
        return
    currentRow += 1
    wordle.guessCheck = getResponse(wordle.guess)
    wordle.GetNextGuess()

def next(wordle):
    global currentRow
    addRow(wordle.guess)

def reset():
    global wordle, currentRow, allButtons
    for btn in allButtons:
        btn.destroy()
    allButtons = []
    wordle = Wordle()
    wordle.loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
    wordle.formatDictionary()
    currentRow = 0
    wordle.main('plumb', '', next)

btn=Button(win,text='NEXT', width=6, height=1, bg="#538d4e", fg="#d7dadc", font=("Arial 10"), command=nextRow)
btn.place(x=16,y=380)

btn=Button(win,text='RESET', width=6, height=1, bg="#b59f3b", fg="#d7dadc", font=("Arial 10"), command=reset)
btn.place(x=257,y=380)

reset()

win.mainloop() #running the loop that works as a trigger