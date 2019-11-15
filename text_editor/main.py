from collections import OrderedDict
import os
import click


_path_folder = os.path.dirname(os.path.abspath(__file__)) + '/documents'
_path_docs = _path_folder + '/{}.txt'

class Editor:
    def __init__(self):
        self.docs = OrderedDict()

        self._editor_commands = 'Commands:\n\n' \
                                'Esc         :   Exit and Discard changes\n' \
                                'CTRL + S    :   Save and Exit\n' \
                                'CTRL + B    :   Bold\n' \
                                'CTRL + I    :   Italic\n' \
                                'CTRL + U    :   Underline\n' \
                                '\n'

        self.valid_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTU' \
                           'VWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

        self.load_docs()

    def open_doc(self, doc_id):
        try:
            doc = self.docs[int(doc_id)]
            self.editor_loop(doc=doc)
        except KeyError:
            click.echo(f'Document ID {doc_id} does not exist')
        return True

    def create_doc(self, doc_name='New Document'):
        new_doc = Document(doc_name=doc_name)
        self.docs[new_doc.id] = new_doc

        click.echo('Successfully created document!\nDocument ID:{}\nDocument Name:{}\n'.format(new_doc.id, doc_name))
        return True

    def load_docs(self):
        files = [file for file in os.listdir(_path_folder) if os.path.isfile(os.path.join(_path_folder, file))]
        files.sort(key=lambda file: os.path.getmtime(os.path.join(_path_folder, file)))

        for file in files:
            file_name, _ = os.path.splitext(file)
            new_doc = Document(doc_name=file_name)

            with open(os.path.join(_path_folder, file), 'r') as file_rd:
                chars = file_rd.read().split()

            for char in chars:
                new_doc.add_char(char)

            self.docs[new_doc.id] = new_doc

    def editor_loop(self, doc):
        while True:
            self._clear()
            click.echo(self._editor_commands)
            click.echo(doc.text)
            c = click.getchar()
            hex_c = ''.join(['\\' + hex(ord(i))[1:] if i not in self.valid_chars else i for i in c])

            if c == '\xe0K':                # Left Arrow
                doc.move(is_right=False)
            elif c == '\xe0M':              # Right Arrow
                doc.move()
            elif hex_c == r'\xd':           # Enter
                doc.add_char('\n')
            elif hex_c == r'\x8':           # Backspace
                doc.del_char()

            elif hex_c == r'\x2':           # Ctrl + B
                click.echo('bold')
            elif hex_c == r'\x9':           # Ctrl + I
                click.echo('italic')
            elif hex_c == r'\x15':          # Ctrl + U
                click.echo('underline')

            elif hex_c == r'\x13':          # Ctrl + S
                doc.save()
                self._clear()
                break
            elif hex_c == r'\x1b':          # Escape
                return

            else:
                # Type Character
                if c in self.valid_chars:
                    doc.add_char(c)

        doc.save()
        self.load_docs()

    def display_all(self):
        self._clear()
        for key, doc in self.docs.items():
            click.echo('Document ID: {}  :   Document Name:  {}.txt'.format(key, doc.name))
        click.echo('')

    @staticmethod
    def _clear():
        os.system('cls')

class Document:
    doc_id = 1

    def __init__(self, doc_name):
        self._id = Document.doc_id
        self._text = []
        self._name = doc_name
        self.pointer = Pointer()

        self.font_style = {'BOLD': [False, ('<b>', '</b>')],
                           'ITALIC': [False, ('<i>', '</i>')],
                           'UNDERLINE': [False, ('<u>', '</u>')]
                            }

        Document.doc_id += 1

    def __str__(self):
        return ''.join(map(str, self._text))

    def save(self):
        with open(_path_docs.format(self._name), 'w+') as file:
            file.write(self.text)

    def add_char(self, value, to_move=True):
        self._text.insert(self.pointer.point, Character(value))

        if to_move:
            self.move()

    def del_char(self):
        try:
            self._text.pop(self.pointer.point - 1)
        except IndexError:
            return

        self.move(is_right=False)

    def move(self, is_right=True):
        if is_right:

            if len(self._text) < self.pointer.point:
                self.add_char(' ', to_move=False)

            self.pointer.point = 1
        else:
            self.pointer.point = -1

    def check_markup(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return ''.join(map(str, self._text))

    @text.setter
    def text(self, value):
        self._text = value


class Pointer:
    def __init__(self):
        self._point = 0

    def select_indices(self):
        pass

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, value: int):
        if self._point != 0 or value > 0:
            self._point += value

class Character:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value
