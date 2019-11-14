from text_editor.menu import Menu
import time


if __name__ == '__main__':
    m = Menu()

    while True:
        option = m.display_options()

        time.sleep(2)
        if not option:
            break
