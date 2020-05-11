import re
from logging import getLogger
from typing import Iterator, List, Match, Pattern, Tuple

logger = getLogger(__name__)


def split_sentences(text: str, eos: str = "EOS\n") -> Iterator[str]:
    """CaboCha(MeCab)分析器にかけられた結果を一文章毎に分割する

    Arguments:
        text {str} -- 複数センテンスを含む解析結果

    Keyword Arguments:
        eos {str} -- 終了文字 (default: {"EOS\n"})

    Yields:
        Iterator[str] -- 終了文字で分割された1文のリスト

    Usage:
        >>> from cucurbita.util import split_sentences
        >>> document="* 0 -1D 1/1 0.000000\n\u3000\t記号,空白,*,*,*,*,\u3000,\u3000,\u3000\n吾輩は猫である\t名詞,固有名詞,一般,*,*,*,吾輩は猫である,ワガハイハネコデアル,ワガハイワネコデアル\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n* 0 2D 0/1 -1.911675\n名前\t名詞,一般,*,*,*,*,名前,ナマエ,ナマエ\nは\t助詞,係助詞,*,*,*,*,は,ハ,ワ\n* 1 2D 0/0 -1.911675\nまだ\t副詞,助詞類接続,*,*,*,*,まだ,マダ,マダ\n* 2 -1D 0/0 0.000000\n無い\t形容詞,自立,*,*,形容詞・アウオ段,基本形,無い,ナイ,ナイ\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n"
        >>> sentences = [e for e in split_sentences(document)]
        >>> sentences[0]
        '* 0 -1D 1/1 0.000000\n\u3000\t記号,空白,*,*,*,*,\u3000,\u3000,\u3000\n吾輩は猫である\t名詞,固有名詞,一般,*,*,*,吾輩は猫である,ワガハイハネコデアル,ワガハイワネコデアル\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n'
    """
    for sentence in text.split(eos):
        if sentence:
            yield sentence + eos


# splitlinesを用いるのでここでのeosには改行がない
def split_chunks(
    parsed_text: str,
    eos: str = "EOS",
    pattern_header: Pattern[str] = re.compile(""),
    pattern_morph: Pattern[str] = re.compile(""),
) -> Iterator[Tuple[str, List[str]]]:
    """CaboChaでパースした文章を文節毎に分割する

    Arguments:
        parsed_text {str} -- 解析結果で一つのヘッダーと単語形態素結果のまとまり

    Keyword Arguments:
        eos {str} -- 区切り文字 (default: {"EOS"})
        pattern_header {Pattern[str]} -- ヘッダー行の正規表現 (default: {re.compile("")})
        pattern_morph {Pattern[str]} -- 単語行の正規表現 (default: {re.compile("")})

    Yields:
        Iterator[Tuple[str, List[str]]] -- 文節毎のヘッダーと単語のリスト

    Usage:
        >>> from cucurbita.util import split_chunks
        >>> sentetce = '* 0 -1D 1/1 0.000000\n\u3000\t記号,空白,*,*,*,*,\u3000,\u3000,\u3000\n吾輩は猫である\t名詞,固有名詞,一般,*,*,*,吾輩は猫である,ワガハイハネコデアル,ワガハイワネコデアル\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n'
        >>> chunks = [e for e in split_chunks(sentetce)]
        >>> chunks[0]
        ('* 0 -1D 1/1 0.000000', ['\u3000\t記号,空白,*,*,*,*,\u3000,\u3000,\u3000', '吾輩は猫である\t名詞,固有名
    """
    if pattern_header == re.compile(""):
        pattern_header = re.compile(r"^\*\ \d+\ (?:-1|\d+)D\ \d+\/\d+\ -?\d+\.\d+$")

    if pattern_morph == re.compile(""):
        pattern_morph = re.compile(r"^[^,]*\t[^,]*(?:,[^,]*){6,}$")

    header = ""
    morphs: List[str] = []

    # parsed_textにeosがない場合に挙動が変わらないようにする
    parsed_text += eos

    for line in parsed_text.splitlines():
        if line == eos:
            yield header, morphs
            break

        elif pattern_header.match(line):
            logger.debug(f"header: {repr(line)}")
            if header:
                yield header, morphs
            header = line
            morphs = []

        elif pattern_morph.match(line):
            logger.debug(f"morph: {repr(line)}")
            morphs.append(line)

        else:
            # header でも morphでもないパターンはログに残しスキップ
            logger.warn(f"undefined pattern: {repr(line)}")
