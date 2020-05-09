import CaboCha
from cucurbita.entities import Doc


class CaboChaParser:
    def __init__(self, *args, parser=CaboCha.Parser):
        self.parser = parser(*args)

    def parse(self, sentence: str) -> str:
        """文章をCaboChaでパースする"""
        tree = self.parser.parse(sentence)
        return tree.toString(CaboCha.FORMAT_LATTICE)


class JPnlp:
    def __init__(self, *args, parser=CaboChaParser):
        self.parser = parser(*args)

    def __call__(self, text):
        result = self.parser.parse(text)
        return Doc(result, text)
