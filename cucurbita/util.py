import re
from logging import getLogger
from typing import Iterator, List, Tuple

logger = getLogger(__name__)

# Usage:
# >>> from cucurbita.util import *
# >>> document="* 0 -1D 1/1 0.000000\n\u3000\t記号,空白,*,*,*,*,\u3000,\u3000,\u3000\n吾輩は猫である\t名詞,固有名詞,一般,*,*,*,吾輩は猫である,ワガハイハネコデアル,ワガハイワネコデアル\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n* 0 2D 0/1 -1.911675\n名前\t名詞,一般,*,*,*,*,名前,ナマエ,ナマエ\nは\t助詞,係助詞,*,*,*,*,は,ハ,ワ\n* 1 2D 0/0 -1.911675\nまだ\t副詞,助詞類接続,*,*,*,*,まだ,マダ,マダ\n* 2 -1D 0/0 0.000000\n無い\t形容詞,自立,*,*,形容詞・アウオ段,基本形,無い,ナイ,ナイ\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n"
# >>> print(document)
# * 0 -1D 1/1 0.000000
# 　      記号,空白,*,*,*,*,　,　,
# 吾輩は猫である  名詞,固有名詞,一般,*,*,*,吾輩は猫である,ワガハイハネコデアル,ワガハイワネコデアル
# 。      記号,句点,*,*,*,*,。,。,。
# EOS
# * 0 2D 0/1 -1.911675
# 名前    名詞,一般,*,*,*,*,名前,ナマエ,ナマエ
# は      助詞,係助詞,*,*,*,*,は,ハ,ワ
# * 1 2D 0/0 -1.911675
# まだ    副詞,助詞類接続,*,*,*,*,まだ,マダ,マダ
# * 2 -1D 0/0 0.000000
# 無い    形容詞,自立,*,*,形容詞・アウオ段,基本形,無い,ナイ,ナイ
# 。      記号,句点,*,*,*,*,。,。,。
# EOS
#
# >>>
# >>> sentences = [e for e in split_sentences(document)]
# >>> sentences[0]
# '* 0 -1D 1/1 0.000000\n\u3000\t記号,空白,*,*,*,*,\u3000,\u3000,\u3000\n吾輩は猫である\t名詞,固有名詞,一般,*,*,*,吾輩は猫である,ワガハイハネコデアル,ワガハイワネコデアル\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n'
# >>> print(sentences[0])
# * 0 -1D 1/1 0.000000
# 　      記号,空白,*,*,*,*,　,　,
# 吾輩は猫である  名詞,固有名詞,一般,*,*,*,吾輩は猫である,ワガハイハネコデアル,ワガハイワネコデアル
# 。      記号,句点,*,*,*,*,。,。,。
# EOS
#
# >>>
# >>> for e in split_chunks(sentences[1]):
# ...   print(e)
# ...
# ('* 0 2D 0/1 -1.911675', ['名前\t名詞,一般,*,*,*,*,名前,ナマエ,ナマエ', 'は\t助詞,係助詞,*,*,*,*,は,ハ,ワ'])
# ('* 1 2D 0/0 -1.911675', ['まだ\t副詞,助詞類接続,*,*,*,*,まだ,マダ,マダ'])
# ('* 2 -1D 0/0 0.000000', ['無い\t形容詞,自立,*,*,形容詞・アウオ段,基本形,無い,ナイ,ナイ', '。\t記号,句点,*,*,*,*,。,。,。'])


def split_sentences(text: str, eos: str = "EOS\n") -> Iterator[str]:
    """"CaboCha(MeCab)分析器にかけられた結果を一文章毎に分割する"""
    for sentence in text.split(eos)[:-1]:
        yield sentence + eos


# splitlinesを用いるのでここでのeosには改行がない
def split_chunks(
    parsed_text: str,
    eos: str = "EOS",
    pattern_header: "AnyStr" = "",
    pattern_morph: "AnyStr" = "",
) -> Iterator[Tuple[str, List[str]]]:
    """CaboChaでパースした文章を文節毎に分割する"""
    if not pattern_header:
        pattern_header = r"^\*\ \d+\ (?:-1|\d+)D\ \d+\/\d+\ -?\d+\.\d+$"

    if not pattern_morph:
        pattern_morph = r"^[^,]*\t[^,]*(?:,[^,]*){6,}$"

    pattern_header = re.compile(pattern_header)
    pattern_morph = re.compile(pattern_morph)

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
