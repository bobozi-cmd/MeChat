import curses, logging, datetime
from curses.textpad import Textbox, rectangle


logging.basicConfig(
    filename=f'mechat_{datetime.datetime.today().strftime("%Y_%m_%d")}.log',
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(levelname)s] - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d-%H:%M:%S",
)

ESC = 27

def init_input_box(input_box: "curses._CursesWindow"):
    input_box.clear()
    rectangle(input_box, 0, 0, 4-2, 50-2)
    input_box.move(1, 1)
    input_box.refresh()

def init_chat_box(chat_box: "curses._CursesWindow"):
    chat_box.clear()
    rectangle(chat_box, 0, 0, 10-2, 50-2)
    chat_box.refresh()

def add_msg(chat_box: "curses._CursesWindow", new_msg: str, limit: int):
    init_chat_box(chat_box)
    for i in range(len(new_msg) // limit + 1):
        y = i + 1
        chat_box.addnstr(y, 1, new_msg[i*limit:], limit)
    chat_box.refresh()

def main(stdscr: "curses._CursesWindow"):
    stdscr.clear()  # clear screen
    stdscr.keypad(True)
    
    # terminal
    stdscr.addstr("MeChat Room\n")
    stdscr.refresh()

    # chat box
    chat_box = curses.newwin(10, 50, 2, 1)
    init_chat_box(chat_box)

    # input box
    input_box = curses.newwin(4, 50, 12, 1)
    init_input_box(input_box)

    input_str = ""
    while True:
        key = stdscr.getch()

        if key == ESC:
            break
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            logging.info(f"-> {input_str}")
            add_msg(chat_box, input_str, 45)
            input_str = ""
            init_input_box(input_box)
        else:
            input_str += chr(key)
            input_box.addnstr(1, 1, input_str[-45:], 45)
            input_box.refresh()

curses.wrapper(main)

