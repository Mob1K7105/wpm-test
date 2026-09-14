import curses
import random
import time

wordl = 20
start = True
duration = 10

def loadlist():
    with open("Oxford 5000.txt", "r") as file:
        words = file.read().splitlines()
        return words

def tracktime(start_time):
    
    elapsed = time.time() - start_time

    if elapsed < duration: 
        return True
    elif elapsed > duration:
        return False

def getstring():
    sentence = ""
    words = loadlist()

    for i in range(wordl):
        word = random.choice(words)
        sentence = sentence + " " + word
        if i == 0: 
            sentence = sentence[1:]
        
    return sentence

def calculate(characters_typed):
    wpm = round(characters_typed / 5 / (duration /60))
    return wpm

def typing_test(stdscr):
    stdscr.clear()
    start_time = time.time()
    target = getstring()
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

        # Draw each character with its color
        for i, character in enumerate(typed):
            if validity.get(i, False):
                stdscr.addstr(4, i, character, curses.color_pair(1))
            else:
                stdscr.addstr(4, i, character, curses.color_pair(2))

        stdscr.refresh()

    return calculate(characters_typed)

def main():
    wpm = curses.wrapper(typing_test)
    print(f'{wpm} wpm')

main()
