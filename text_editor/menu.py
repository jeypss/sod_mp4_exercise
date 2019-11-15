import time
import click
import os
from .main import Editor


class Menu:
    def __init__(self):
        self._editor = Editor()

        self._options = {'1': self._editor.create_doc,
                         '2': self._editor.open_doc,
                         '3': self._close}

        self._str_options = 'Please select an option number:\n' \
                            '1  -   Create New Document\n' \
                            '2  -   Open an existing Document\n' \
                            '3  -   Exit Program\n'

    def display_options(self):
        self._clear()
        choice = input(self._str_options)

        try:
            if choice == '1':
                param = input('Please type in a valid document file name: ')
                state = self._options[choice](param)
            elif choice == '2':
                self._editor.display_all()
                param = input('Please type in a valid document ID: ')
                state = self._options[choice](param)
            else:
                state = self._options[choice]()
            return state
        except (KeyError, ValueError):
            print('Invalid Option! Please enter a valid option number.')
            time.sleep(2)
            self.display_options()

    def _back(self):
        self.display_options()

    @staticmethod
    def _clear():
        os.system('cls')

    @staticmethod
    def _close():
        time.sleep(2)
        print('Closing Program...')
        return False
