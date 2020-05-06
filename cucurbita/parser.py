import re
from logging import getLogger

from typing import Tuple, List, Iterator, TypeVar, Union

import CaboCha

logger = getLogger(__name__)

SRE_Match = TypeVar(type(re.match("", "")).__name__)


class CaboChaParser:
    pattern_header = r"^\*\ \d+\ (?:-1|\d+)D\ \d+\/\d+\ -?\d+\.\d+$"
    pattern_morph = r"^[^,]*\t[^,]*(?:,[^,]*){8}$"

    def __init__(
        self,
        *args,
        parser=CaboCha.Parser,
        pattern_header: str = "",
        pattern_morph: str = "",
    ):
        self.parser = parser(*args)
        if pattern_header:
            self.pattern_header = pattern_header
        if pattern_morph:
            self.pattern_morph = pattern_morph

    def parse(self, sentence: str) -> str:
        """文章をCaboChaでパースする"""
        tree = self.parser.parse(sentence)
        return tree.toString(CaboCha.FORMAT_LATTICE)

    def is_morph(self, line: str) -> Union[SRE_Match, None]:
        """パースした文章のうちの1行が形態素解析の結果であるか"""
        return re.match(self.pattern_morph, line)

    def is_header(self, line: str) -> Union[SRE_Match, None]:
        """パースした文章のうちの1行が文節情報であるか"""
        return re.match(self.pattern_header, line)

    @classmethod
    def split_chunks(
        cls, parsed_text: str, *, eos="EOS"
    ) -> Iterator[Tuple[str, List[str]]]:
        """CaboChaでパースした文章を文節毎に分割する"""
        header = ""
        morphs = []
        for line in parsed_text.splitlines():
            if line == eos:
                yield header, morphs
                break

            elif cls.is_header(cls, line):
                logger.debug(f"header: {line}")
                if header:
                    yield header, morphs
                header = line
                morphs = []

            elif cls.is_morph(cls, line):
                logger.debug(f"morph: {line}")
                morphs.append(line)

            else:
                logger.warn(f"undefined pattern: {line}")


if __name__ == "__main__":
    ccp = CaboChaParser()
    parsed = ccp.parse("隣の客はよく柿食う客だ。")
    for chunk in ccp.split_chunks(parsed):
        print(chunk)
