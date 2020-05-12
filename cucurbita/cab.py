from logging import getLogger
from typing import Iterator, List, Tuple, Union

from cucurbita.util import split_chunks, split_words

logger = getLogger(__name__)


class Morph(object):
    """CaboCha(MeCab)による形態素解析結果を受け取り、オブジェクトを返す

    Arguments:
        line {str} -- 形態素解析結果の1行 (ipadic 辞書を想定)

    Attributes:
        surface  {str} -- 表層系
        pos (str)  {str} -- 品詞
        pos1  (str)  {str} -- 品詞詳細1
        pos2  (str)  {str} -- 品詞詳細2
        pos3  (str)  {str} -- 品詞詳細3
        conj_form  (str)  {str} -- 活用形
        conj  (str)  {str} -- 活用型
        base  (str)  {str} -- 基本形
        yomi  (str)  {str} -- 読み
        pron (str)  {str} -- 発音

    Usage:
        >>> from cucurbita.cab import Morph
        >>> morph = "surface\tpos,pos1,pos2,pos3,conj_form,conj,base,yomi,pron"
        >>> m = Morph(morph)
        >>> m.surface
        'surface'
        >>> m.surface
    """

    def __init__(self, line: str) -> None:
        try:
            self.values = split_words(line)
        except AssertionError:
            logger.warn(f"InvalidLinePattern: {repr(line)}")
            return

        self.surface = self.values[0]
        self.pos = self.values[1]
        self.pos1 = self.values[2]
        self.pos2 = self.values[3]
        self.pos3 = self.values[4]
        self.conj_form = self.values[5]
        self.conj = self.values[6]
        self.base = self.values[7]
        self.yomi = self.values[8]
        self.pron = self.values[9]

    def __str__(self) -> str:
        return str(self.surface)

    def __repr__(self) -> str:
        return f"<Morph: {self.surface}>"


# class Chunk(object):
#     """文節オブジェクト

#     単語オブジェクトを格納する

#     Args:
#         header (str): 文節解析結果のヘッダー\n
#             e.g. "* 0 2D 0/1 -1.911675"\n
#         morphs (List[str]): 文節解析結果の単語の配列\n
#             e.g. ["名前\\t名詞,一般,*,*,*,*,名前,ナマエ,ナマエ\\n", "は\\t助詞,係助詞,*,*,*,*,は,ハ,ワ"]\n

#     Attributes:
#         pos (int): 文章内での文節番号\n
#         dst (int): かかる文節番号\n
#         score (float): かかり度合い\n
#         morphs (list_iterator): 単語オブジェクト(Morph)の配列\n

#     Usage:
#         >>> header = "* 0 2D 0/1 -1.911675\\n"
#         >>> morphs = ["名前\\t名詞,一般,*,*,*,*,名前,ナマエ,ナマエ\\n", "は\\t助詞,係助詞,*,*,*,*,は,ハ,ワ\\n"]
#         >>> chunk = Chunk(header, morphs)
#         >>> chunk
#         <Chunk: [<Morph: 名前>, <Morph: は>]>
#         >>> chunk.morphs
#         [<Morph: 名前>, <Morph: は>]
#         >>> c.pos, c.dst, c.score
#         (0, 2, -1.911675)
#     """

#     def __init__(self, header: str, morphs: List[str]) -> None:
#         if header:
#             self.pos, self.dst, self.score = self.__split_words(header)
#         else:
#             self.pos = self.dst = self.score = 0
#         self.morphs = list(self.__parse_morphs(morphs))

#     def __str__(self) -> str:
#         return " ".join(map(str, self.morphs))

#     def __repr__(self) -> str:
#         return f"<Chunk: {self.morphs}>"

#     def __split_words(self, line: str) -> Tuple[int, int, float]:
#         _, pos, dst, _, score, *_ = line.split()
#         if not dst.endswith("D"):
#             raise Exception("Undefined format")
#         dst = dst.rstrip("D")
#         return int(pos), int(dst), float(score)

#     def __parse_morphs(self, morphs: List[str]) -> Iterator["Morph"]:
#         for morph in morphs:
#             yield Morph(morph)


# class Sect(Cab):
#     # self.chunks = list(self.__parse_chunks(result))
#     def __str__(self):
#         return " / ".join(map(str, self.chunks))

#     def __repr__(self):
#         return f"<Sect: {self.chunks}>"

#     def __parse_chunks(self, text):
#         for chunk in split_chunks(text):
#             yield Chunk(*chunk)

#     def to_doc(self):
#         return Doc(self.result, self.text)


# class Doc(Cab):
#     def __str__(self) -> str:
#         return self.text

#     def __repr__(self) -> str:
#         return f"<Doc: {self.text}>"

#     def to_sect(self)->Sect:
#         return Sect(self.result, self.text)


# class Cab(object):

#     def __init__(self, result: str, text: str = "") -> None:
#         self.result = result
#         self.text = text if text else self.__get_surface(result)

#     def __get_surface(self, text: str) -> str:
#         """形態素解析結果から表層系だけを抜き出す"""
#         surface = ""
#         for line in text.splitlines():
#             if len(line) == 2:
#                 surface += line[0]
#         return surface

#     def tokenize(self) -> List[Morph]:
#         """形態素解析結果からmorphsの配列を生成する"""
#         tokens = [morphs for _, morphs in split_chunks(self.result)]
#         return [Morph(token) for token in tokens]
