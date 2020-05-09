from logging import getLogger
from typing import Iterator, List, Tuple

from cucurbita.util import split_chunks

logger = getLogger(__name__)


class Morph(object):
    """CaboCha(MeCab)による形態素解析結果を受け取り、オブジェクトを返す
    
    Args:
        line (str): 形態素解析結果の1行 (ipadic 辞書を想定)

    Attributes:
        surface  (str): 表層系\n
        pos (str) ※1: 品詞\n
        pos1  (str) ※1: 品詞詳細1\n
        pos2  (str) ※1: 品詞詳細2\n
        pos3  (str) ※1: 品詞詳細3\n
        conj_form  (str) ※1: 活用形\n
        conj  (str) ※1: 活用型\n
        base  (str) ※1: 基本形\n
        yomi  (str) ※1: 読み\n
        pron (str) ※1: 発音\n

        is_valid (bool): 有効な変換結果であるか
        
        ※1: is_valid = False のとき AttributeError の可能性がある

    Raises:
        AttributeError: when is_valid == False

    Usage:
        >>> m = Morph('走っ\\t動詞,自立,*,*,五段・ラ行,連用タ接続,走る,ハシッ,ハシッ')
        >>> m
        <Morph: 走っ>
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

    def __init__(self, line: str) -> None:
        self.values = self.__split_words(line)
        if len(self.values) == len(self.columns):
            self.is_valid = True
        else:
            self.is_valid = False
            logger.warn(f"InvalidLinePattern: {line}")
        for col, value in zip(self.columns, self.values):
            exec(f"self.{col} = '{value}'")

    def __str__(self) -> str:
        return self.surface

    def __repr__(self) -> str:
        return f"<Morph: {self.surface}>"

    def __split_words(self, line: str) -> List[str]:
        """カンマとタブで分割"""
        return sum([e.split(",") for e in line.rstrip("\n").split("\t")], [])


class Chunk(object):
    """文節オブジェクト

    単語オブジェクトを格納する

    Args:
        header (str): 文節解析結果のヘッダー\n
            e.g. "* 0 2D 0/1 -1.911675"\n
        morphs (List[str]): 文節解析結果の単語の配列\n　
            e.g. ["名前\\t名詞,一般,*,*,*,*,名前,ナマエ,ナマエ\\n", "は\\t助詞,係助詞,*,*,*,*,は,ハ,ワ"]\n

    Attributes:
        pos (int): 文章内での文節番号\n
        dst (int): かかる文節番号\n
        score (float): かかり度合い\n
        morphs (list_iterator): 単語オブジェクト(Morph)の配列\n

    Usage:
        >>> header = "* 0 2D 0/1 -1.911675\\n"
        >>> morphs = ["名前\\t名詞,一般,*,*,*,*,名前,ナマエ,ナマエ\\n", "は\\t助詞,係助詞,*,*,*,*,は,ハ,ワ\\n"]
        >>> chunk = Chunk(header, morphs)
        >>> chunk
        <Chunk: [<Morph: 名前>, <Morph: は>]>
        >>> chunk.morphs
        [<Morph: 名前>, <Morph: は>]
        >>> c.pos, c.dst, c.score
        (0, 2, -1.911675)
    """

    def __init__(self, header: str, morphs: List[str]) -> None:
        if header:
            self.pos, self.dst, self.score = self.__split_words(header)
        else:
            self.pos = self.dst = self.score = 0
        self.morphs = list(self.__parse_morphs(morphs))

    def __str__(self) -> str:
        return " ".join(map(str, self.morphs))

    def __repr__(self) -> str:
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
        # TODO: 引数をDocに合わせる
        self.text = text
        self.result = result
        self.chunks = list(self.__parse_chunks(result))

    def __str__(self):
        return " / ".join(map(str, self.chunks))

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
    """

    Usage:
        >>> sentence="* 0 2D 0/1 -1.911675\n\
        ... 名前\t名詞,一般,*,*,*,*,名前,ナマエ,ナマエ\n\
        ... は\t助詞,係助詞,*,*,*,*,は,ハ,ワ\n\
        ... * 1 2D 0/0 -1.911675\n\
        ... まだ\t副詞,助詞類接続,*,*,*,*,まだ,マダ,マダ\n\
        ... * 2 -1D 0/0 0.000000\n\
        ... 無い\t形容詞,自立,*,*,形容詞・アウオ段,基本形,無い,ナイ,ナイ\n\
        ... 。\t記号,句点,*,*,*,*,。,。,。\n\
        ... EOS\n"
        >>> 
        >>> doc = Doc(sentence)
        >>> doc
        <Doc: 名前はまだ無い。>
        >>> 
        >>> doc.tokenize()
        [<Morph: 名前>, <Morph: は>, <Morph: まだ>, <Morph: 無い>, <Morph: 。>]
        >>> 
        >>> doc.to_sect()
        <Sect: [<Chunk: [<Morph: 名前>, <Morph: は>]>, <Chunk: [<Morph: まだ>]>, <Chunk: [<Morph: 無い>, <Morph: 。>]>]>

    """

    def __init__(self, result, text=""):
        # TODO: eos 設定(resultが複数のEOSを含む場合の__get_surfaceの挙動がおかしい)
        self.text = text if text else "".join(self.__get_surface(result))
        self.result = result

    def __call__(self, result, text=""):
        self.text = text if text else "".join(self.__get_surface(result))
        self.result = result

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"<Doc: {self.text}>"

    def __get_surface(self, text):
        surface = []
        for line in text.splitlines():
            line = line.split("\t")
            if len(line) == 2:
                surface.append(line[0])
        return surface

    def to_sect(self):
        return Sect(self.text, self.result)

    def tokenize(self):
        morphs = sum([morphs for _, morphs in split_chunks(self.result)], [])
        return [Morph(morph) for morph in morphs]
