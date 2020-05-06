import CaboCha


class CaboChaParser:
    def __init__(self, *args, parser=CaboCha.Parser):
        self.parser = parser(*args)

    def parse(self, sentence: str) -> str:
        """文章をCaboChaでパースする"""
        tree = self.parser.parse(sentence)
        return tree.toString(CaboCha.FORMAT_LATTICE)
