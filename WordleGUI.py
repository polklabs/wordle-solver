from time import sleep
from tkinter import *
from Wordle import formatDictionary, main, loadDictionary

loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)
formatDictionary()

win=Tk() #creating the main window and storing the window object in 'win'
win.title('Wordle') #setting title of the window
win.geometry('325x600') #setting the size of the window
win.configure(bg="white")

currentRow = 0
row = []
rowState = []

def func(btnRow, column):#function of the button
    global currentRow, rowState, row
    if btnRow != currentRow:
        return
    rowState[column] += 1
    rowState[column] = rowState[column] % 3
    if rowState[column] == 0:
        row[column]['bg'] = "lightgrey"
    if rowState[column] == 1:
        row[column]['bg'] = "yellow"
    if rowState[column] == 2:
        row[column]['bg'] = "lightgreen"

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


def addRow(guess):
    global currentRow, row, rowState
    for i in range(len(guess)):
        char = guess[i]
        btn=Button(win,text=str(char).upper(), width=4, height=2, bg="lightgrey", command=lambda i=i:func(currentRow, i))
        btn.place(x=20+(i*60),y=30)
        row.append(btn)
        rowState.append(0)

def nextRow():
    global currentRow
    currentRow += 1

def next(guess, word, t):
    global currentRow
    addRow(guess)
    while currentRow == t:
        sleep(1)
        print('Sleep')
    return getResponse(guess)

btn=Button(win,text='Submit', width=4, height=2, bg="lightgrey", command=nextRow)
btn.place(x=200,y=60)

word = 'plumb'
main(word, '', next)

win.mainloop() #running the loop that works as a trigger