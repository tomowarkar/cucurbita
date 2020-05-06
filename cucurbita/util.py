import re
from logging import getLogger

from typing import Tuple, List, Iterator

logger = getLogger(__name__)


def split_chunks(
    parsed_text: str, *, eos="EOS", pattern_header: str = "", pattern_morph: str = ""
) -> Iterator[Tuple[str, List[str]]]:
    """CaboChaでパースした文章を文節毎に分割する"""
    if not pattern_header:
        pattern_header = r"^\*\ \d+\ (?:-1|\d+)D\ \d+\/\d+\ -?\d+\.\d+$"

    if not pattern_morph:
        pattern_morph = r"^[^,]*\t[^,]*(?:,[^,]*){6,}$"

    pattern_header = re.compile(pattern_header)
    pattern_morph = re.compile(pattern_morph)

    header = ""
    morphs = []
    for line in parsed_text.splitlines():
        if line == eos:
            yield header, morphs
            break

        elif pattern_header.match(line):
            logger.debug(f"header: {line}")
            if header:
                yield header, morphs
            header = line
            morphs = []

        elif pattern_morph.match(line):
            logger.debug(f"morph: {line}")
            morphs.append(line)

        else:
            logger.warn(f"undefined pattern: {line}")
