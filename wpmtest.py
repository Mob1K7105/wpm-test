import curses
import random
import time
from tabulate import tabulate
from interactive_buttons import Button, Component
import os
from pathlib import Path

wordl = 20
start = True
duration = 10
dir = Path(__file__).resolve().parent

def get_info():
    try:
        time = int(input("Duration: "))
    except time > 60:
        print("Pick a smaller time duration")

    global duration
    duration = time

    options = []
    
    for file in os.listdir(dir):
        if file.endswith('.txt'):
            options.append(file)
    
    for element in options:
        buttons = [Button(label = element, value = element)]
    
    comp   = Component(buttons)
    choice = comp.column_buttons()

    return choice 


def loadlist(value):
    with open(value, "r") as file:
        words = file.read().splitlines()
        return words

def tracktime(start_time):
    
    elapsed = time.time() - start_time

    if elapsed < duration: 
        return True
    elif elapsed > duration:
        return False

def getstring(value):
    sentence = ""
    words = loadlist(value)

    for i in range(wordl):
        word = random.choice(words)
        sentence = sentence + " " + word
        if i == 0: 
            sentence = sentence[1:]
        
    return sentence

def calculate(characters_typed):
    wpm = round(characters_typed / 5 / (duration / 60))
    return wpm

def accuracy(validity):
    typed = 0
    correct = 0
    for element in validity.values():
        typed += 1
        if element == True: 
            correct += 1
    accuracy = round((correct / typed) * 100)
    errors = typed - correct
    return (accuracy, errors)

def typing_test(stdscr, target):
    stdscr.clear()
    start_time = time.time()
    stdscr.addstr(0, 0, f"Target:{target}:")
    typed = ""

    curses.start_color()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)


    while tracktime(start_time):

        remaining = duration - (time.time() - start_time)
        stdscr.addstr(2, 0, f'{remaining:.1f}s remaining   ')

        stdscr.timeout(50)

        try:
            key = stdscr.getkey()
        except curses.error:
            key = None

        if key == "KEY_BACKSPACE":
            typed = typed[:-1]
        elif key is not None and len(key) == 1 and key.isprintable():
            typed += key
                
        if key == "\x1b": #Escape
            break

        validity = {}
        characters_typed = 0

        for i, character in enumerate(typed):
            if i < len(target):
                if character == target[i]:
                    validity[i] = True
                    characters_typed += 1
                else:
                    validity[i] = False

        stdscr.move(4, 0)
        stdscr.clrtoeol()

        height, width = stdscr.getmaxyx()

        for i, character in enumerate(typed):
            row = 4 + (i // width)
            col = i % width

            if row >= height:
                break


            color = curses.color_pair(1) if validity.get(i, False) else curses.color_pair(2)
            stdscr.addstr(row, col, character, color)


        stdscr.refresh()

    acc, errors = accuracy(validity)

    return calculate(characters_typed), acc, errors


def main():
    value = get_info()
    target = getstring(value)
    wpm = curses.wrapper(typing_test, target)
    print(tabulate(
    [[wpm[0], wpm[1], wpm[2]]], 
    headers=['WPM', 'Accuracy (%)', '# of errors']))

main()
