import itertools
from logging import getLogger
from typing import Iterator, List, Tuple, Union

from cucurbita.util import split_chunks, split_words

logger = getLogger(__name__)


class Morph(object):
    """CaboCha(MeCab)による形態素解析結果を受け取り、オブジェクトを返す

    Arguments:
        line {str} -- 形態素解析結果の1行 (ipadic 辞書を想定)

    Attributes:
        surface {str} -- 表層系
        pos {str} -- 品詞
        pos1 {str} -- 品詞詳細1
        pos2 {str} -- 品詞詳細2
        pos3 {str} -- 品詞詳細3
        conj_form {str} -- 活用形
        conj {str} -- 活用型
        base {str} -- 基本形
        yomi {str} -- 読み
        pron {str} -- 発音

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


class Chunk(object):
    """文節オブジェクト

    Arguments:
        header {str} -- 文節解析結果のヘッダー
        morphs {List[str]} -- 文節解析結果の単語の配列

    Attributes:
        pos {int} -- 文節内での位置(文節番号)
        dst {int} -- かかる対象の文節番号
        score {float} -- 係度合い
        morphs {List[Morph]} -- 構成する単語

    Raises:
        Exception -- ヘッダ行のフォーマットがおかしい場合

    Usage:
        >>> from cucurbita.cab import Chunk
        >>> header = "* 0 2D 0/1 -1.911675"
        >>> morphs = ["surface\tpos,pos1,pos2,pos3,conj_form,conj,base,yomi,pron"]
        >>> c = Chunk(morphs=morphs, header=header)
        >>> c.pos
        0
    """

    def __init__(self, morphs: List[str], header: str = "") -> None:
        if header:
            self.pos, self.dst, self.score = self.__parse_header(line=header)
        else:
            self.pos = self.dst = self.score = 0
        self.morphs = [Morph(line=morph) for morph in morphs]

    def __str__(self) -> str:
        return "".join(map(str, self.morphs))

    def __repr__(self) -> str:
        return "<Chunk: {}>".format(" ".join(map(str, self.morphs)))

    def __parse_header(self, line: str) -> Tuple[int, int, float]:
        _, pos, dst, _, score, *_ = line.split()
        if not dst.endswith("D"):
            raise Exception("Undefined format")
        dst = dst.rstrip("D")
        return int(pos), int(dst), float(score)


class Cab(object):
    """Cab(CaboCha, MeCab)解析用ベースクラス

    Arguments:
        result {str} -- CaboCha, MeCab解析結果
        text {str} -- CaboCha, MeCab解析元本文

    Attributes:
        result {str} -- CaboCha, MeCab解析結果
        text {str} -- CaboCha, MeCab解析元本文

    """

    def __init__(self, result: str, text: str = "") -> None:
        self.result = result
        self.text = text if text else self.__get_surface(result)

    def __get_surface(self, text: str) -> str:
        """形態素解析結果から表層系だけを抜き出す"""
        surface = ""
        for line in text.splitlines():
            line = line.split("\t")
            if len(line) == 2:
                surface += line[0]
        return surface

    def tokenize(self) -> List[Morph]:
        """形態素解析結果からmorphsの配列を生成する"""
        tokens = []
        for _, morphs in split_chunks(self.result):
            tokens += morphs
        return [Morph(token) for token in tokens]


class Sect(Cab):
    """cabocha用インターフェイス

    Arguments:
        result {str} -- CaboCha解析結果
        text {str} -- CaboCha解析元本文

    Attributes:
        result {str} -- CaboCha解析結果
        text {str} -- CaboCha解析元本文
        chunks {List[Chunk]} -- 文節集合

    Usage:
        >>> from cucurbita.cab import Chunk

    """

    def __init__(self, result: str, text: str = "") -> None:
        super().__init__(result=result, text=text)
        self.chunks = [
            Chunk(morphs=morphs, header=header)
            for header, morphs in split_chunks(result)
        ]

    def __str__(self) -> str:
        return "".join(map(str, self.chunks))

    def __repr__(self) -> str:
        return "<Sect: {}>".format(" / ".join(map(str, self.chunks)))


class Doc(Cab):
    """mecab用インターフェイス

    Arguments:
        result {str} -- MeCab解析結果
        text {str} -- MeCab解析元本文

    Attributes:
        result {str} -- MeCab解析結果
        text {str} -- MeCab解析元本文

    Usage:
        >>> from cucurbita.cab import Doc

    """

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<Doc: {self.text}>"
