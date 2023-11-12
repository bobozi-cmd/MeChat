import curses

def main(stdscr):
    # 清空屏幕
    stdscr.clear()

    # 设置终端窗口
    stdscr.addstr("聊天室\n")
    stdscr.refresh()

    # 创建输入框
    input_box = curses.newwin(1, 50, 3, 1)
    input_box.addstr(0, 0, "请输入消息：")
    input_box.refresh()

    # 创建聊天框
    chat_box = curses.newwin(10, 50, 5, 1)
    chat_box.addstr(0, 0, "聊天内容：")
    chat_box.refresh()

    # 获取用户输入
    while True:
        key = stdscr.getch()

        # 当用户按下回车键时，获取输入框中的消息
        if key == curses.KEY_ENTER or key in [10, 13]:
            message = input_box.getstr(0, len("请输入消息："), 40)
            chat_box.addstr(2, 1, message)
            input_box.clear()
            input_box.addstr(0, len("请输入消息："), " " * 40)
            input_box.refresh()
            chat_box.refresh()

        # 当用户按下ESC键时，退出程序
        elif key == 27:
            break

curses.wrapper(main)