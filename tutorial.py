import curses
import time
import random


def show_start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test! Press any key to begin.")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm = 0):
    stdscr.addstr(target)
    stdscr.addstr(2, 0, f"Words per minute: {wpm}")
    stdscr.addstr(4, 0, "Press ESC to exit.")

    for i, char in enumerate(current):
        correct_char = target[i]
        
        if char == correct_char:
            color = curses.color_pair(1)
        else:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip() # strip removes the EOL character

def is_key_escape(key):
    if ord(key) == 27:
        return True
    else:
        return False
    
def is_key_backspace(key):
    if ord(key) == 8:
        return True
    else:
        return False
    
def calculate_wpm(n_characters, time_elapsed):
    try:
        return ((n_characters / time_elapsed * 60) / 5) # assumption: average word has 5 characters
    except ZeroDivisionError:
        return 0

def show_test_screen(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)
    
    while True:
        wpm = round(calculate_wpm(len(current_text), time.time() - start_time))

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if is_key_escape(key):
            break

        if is_key_backspace(key):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    show_start_screen(stdscr)

    while True:
        show_test_screen(stdscr)
        stdscr.addstr(4, 0, "You completed the test. Press any key to continue. Press ESC to exit.")
        key = stdscr.getkey()
        if is_key_escape(key):
            break

curses.wrapper(main)
