from logging import getLogger

from typing import List, Tuple, Iterator

from cucurbita.util import split_chunks
from cucurbita.cabocha import CaboChaParser

logger = getLogger(__name__)


class Morph:
    """CaboCha(MeCab)による形態素解析結果を受け取り、オブジェクトを返す
  Args:
    line (str): 形態素解析結果の1行 (ipadic 辞書を想定)

  Attributes:
    surface  (str): 表層系
    pos (str) ※1: 品詞
    pos1  (str) ※1: 品詞詳細1
    pos2  (str) ※1: 品詞詳細2
    pos3  (str) ※1: 品詞詳細3
    conj_form  (str) ※1: 活用形
    conj  (str) ※1: 活用型
    base  (str) ※1: 基本形
    yomi  (str) ※1: 読み
    pron (str) ※1: 発音

    is_valid (bool): 有効な形態素解析結果であるか
    
    ※1: is_valid = False のとき AttributeError の可能性がある

  Usage:
    >>> m = Morph('走っ\t動詞,自立,*,*,五段・ラ行,連用タ接続,走る,ハシッ,ハシッ')
    >>> m
    走っ
    >>> m.pos
    '動詞'
    >>> m.base
    '走る'
  """

    columns = [
        "surface",
        "pos",
        "pos1",
        "pos2",
        "pos3",
        "conj_form",
        "conj",
        "base",
        "yomi",
        "pron",
    ]

    def __init__(self, line: str):
        self.values = self.__split_words(line)
        if len(self.values) == len(self.columns):
            self.is_valid = True
        else:
            self.is_valid = False
            logger.warn(f"InvalidLinePattern: {line}")
        for col, value in zip(self.columns, self.values):
            exec(f"self.{col} = '{value}'")

    def __str__(self):
        return self.surface

    def __repr__(self):
        return f"<Morph: {self.surface}>"

    def __split_words(self, line: str) -> List[str]:
        """カンマとタブで分割"""
        return sum([e.split(",") for e in line.split("\t")], [])


class Chunk:
    def __init__(self, header: str, morphs: List[str]):
        if header:
            self.pos, self.dst, self.score = self.__split_words(header)
        else:
            self.pos = self.dst = self.score = 0
        self.morphs = list(self.__parse_morphs(morphs))

    def __str__(self):
        return " ".join(map(str, self.morphs))

    def __repr__(self):
        return f"<Chunk: {self.morphs}>"

    def __split_words(self, line: str) -> Tuple[int, int, float]:
        _, pos, dst, _, score, *_ = line.split()
        if not dst.endswith("D"):
            raise Exception("Undefined format")
        dst = dst.rstrip("D")
        return int(pos), int(dst), float(score)

    def __parse_morphs(self, morphs: List[str]) -> Iterator["Morph"]:
        for morph in morphs:
            yield Morph(morph)


class Sect:
    def __init__(self, text, result):
        self.text = text
        self.result = result
        self.chunks = list(self.__parse_chunks(result))

    def __str__(self):
        return " ".join(map(str, self.chunks))

    def __repr__(self):
        return f"<Sect: {self.chunks}>"

    def __parse_chunks(self, text):
        for chunk in split_chunks(text):
            yield Chunk(*chunk)

    def tokens(self):
        return sum([chunk.morphs for chunk in self.chunks], [])

    def dependency(self):
        d = {}
        for pos, dst in self.relation():
            if d.get(dst):
                d[dst].append(pos)
            else:
                d[dst] = [pos]
        return d

    def relation(self):
        return [(c.pos, c.dst) for c in self.chunks]


class Doc:
    def __init__(self, text, result):
        self.text = text
        self.result = result

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"<Doc: {self.text}>"

    def to_sect(self):
        return Sect(self.text, self.result)

    def tokenize(self):
        morphs = sum([morphs for _, morphs in split_chunks(self.result)], [])
        return [Morph(morph) for morph in morphs]


class JPnlp:
    def __init__(self, *args, parser=CaboChaParser):
        self.parser = parser(*args)

    def __call__(self, text):
        text = text.rstrip("\n")
        result = self.parser.parse(text)
        return Doc(text, result)
