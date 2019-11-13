class Editor:
    def __init__(self):
        self.docs = {}

    def open_doc(self, doc_id):
        try:
            doc = self.docs[doc_id]
            return doc
        except KeyError:
            print(f'Document ID {doc_id} does not exist')

    def create_doc(self, doc_name='New Document'):
        new_doc = Document(doc_name=doc_name)
        self.docs[new_doc.id] = new_doc

        return self.open_doc(doc_id=new_doc.id)

    def close(self):
        pass


class Document:
    doc_id = 0

    def __init__(self, doc_name):
        self._id = Document.doc_id
        self._text = []
        self.doc_name = doc_name
        self.pointer = Pointer()

        Document.doc_id += 1

    def __str__(self):
        return ''.join(map(str, self._text))

    def save(self):
        pass

    def add_char(self, value):
        self._text.insert(self.pointer.point, Character(value))

    def del_char(self):
        self._text.pop(self.pointer.point)

    def update(self, is_right: bool):
        if is_right:
            self.pointer.point = 1


    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return ''.join(self._text)


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
        self._point += value


class Character:
    def __init__(self, value):
        self.value = value
        self.tagger = Markup()
        self.style = {}

    def __repr__(self):
        return self.value


class Markup:
    def __init__(self):
        self.tags = {}


test = Editor()
d = test.create_doc()
d.add_char('a')
d.add_char('b')
print(d)
