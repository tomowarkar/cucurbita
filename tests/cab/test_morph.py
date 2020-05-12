import pytest

from cucurbita.cab import Morph

morph1 = "隣\t名詞,一般,*,*,*,*,隣,トナリ,トナリ"
morph2 = "surface\tpos,pos1,pos2,pos3,conj_form,conj,base"


@pytest.mark.parametrize(
    "pin, pout",
    [
        (morph1, "隣"),
        (morph1 + "\n", "隣"),
        (morph2, "surface"),
        (morph2 + "\n", "surface"),
    ],
)
def test_morph_default_surface(pin, pout):
    m = Morph(pin)
    assert m.surface == pout


@pytest.mark.parametrize(
    "pin, pout",
    [(morph1, "名詞"), (morph1 + "\n", "名詞"), (morph2, "pos"), (morph2 + "\n", "pos")],
)
def test_morph_default_pos(pin, pout):
    m = Morph(pin)
    assert m.pos == pout


@pytest.mark.parametrize(
    "pin, pout",
    [(morph1, "一般"), (morph1 + "\n", "一般"), (morph2, "pos1"), (morph2 + "\n", "pos1")],
)
def test_morph_default_pos1(pin, pout):
    m = Morph(pin)
    assert m.pos1 == pout


@pytest.mark.parametrize(
    "pin, pout",
    [(morph1, "*"), (morph1 + "\n", "*"), (morph2, "pos2"), (morph2 + "\n", "pos2")],
)
def test_morph_default_pos2(pin, pout):
    m = Morph(pin)
    assert m.pos2 == pout


@pytest.mark.parametrize(
    "pin, pout",
    [(morph1, "*"), (morph1 + "\n", "*"), (morph2, "pos3"), (morph2 + "\n", "pos3")],
)
def test_morph_default_pos3(pin, pout):
    m = Morph(pin)
    assert m.pos3 == pout


@pytest.mark.parametrize(
    "pin, pout",
    [
        (morph1, "*"),
        (morph1 + "\n", "*"),
        (morph2, "conj_form"),
        (morph2 + "\n", "conj_form"),
    ],
)
def test_morph_default_conj_form(pin, pout):
    m = Morph(pin)
    assert m.conj_form == pout


@pytest.mark.parametrize(
    "pin, pout",
    [(morph1, "*"), (morph1 + "\n", "*"), (morph2, "conj"), (morph2 + "\n", "conj")],
)
def test_morph_default_conj(pin, pout):
    m = Morph(pin)
    assert m.conj == pout


@pytest.mark.parametrize(
    "pin, pout",
    [(morph1, "隣"), (morph1 + "\n", "隣"), (morph2, "base"), (morph2 + "\n", "base")],
)
def test_morph_default_base(pin, pout):
    m = Morph(pin)
    assert m.base == pout


@pytest.mark.parametrize(
    "pin, pout",
    [(morph1, "トナリ"), (morph1 + "\n", "トナリ"), (morph2, None), (morph2 + "\n", None)],
)
def test_morph_default_yomi(pin, pout):
    m = Morph(pin)
    assert m.yomi == pout


@pytest.mark.parametrize(
    "pin, pout",
    [(morph1, "トナリ"), (morph1 + "\n", "トナリ"), (morph2, None), (morph2 + "\n", None)],
)
def test_morph_default_pron(pin, pout):
    m = Morph(pin)
    assert m.pron == pout


@pytest.mark.parametrize(
    "pin, pout",
    [
        (
            "走っ\t動詞,自立,*,*,五段・ラ行,連用タ接続,走る,ハシッ,ハシッ",
            ["走っ", "動詞", "自立", "*", "*", "五段・ラ行", "連用タ接続", "走る", "ハシッ", "ハシッ"],
        ),
        (
            "走っ\t動詞,自立,*,*,五段・ラ行,連用タ接続,走る,ハシッ,ハシッ\n",
            ["走っ", "動詞", "自立", "*", "*", "五段・ラ行", "連用タ接続", "走る", "ハシッ", "ハシッ"],
        ),
        (
            "走っ\t動詞,自立,*,*,五段・ラ行,連用タ接続,走る",
            ["走っ", "動詞", "自立", "*", "*", "五段・ラ行", "連用タ接続", "走る", None, None],
        ),
    ],
)
def test_morph(pin, pout):
    m = Morph(pin)
    assert m.surface == pout[0]
    assert m.pos == pout[1]
    assert m.pos1 == pout[2]
    assert m.pos2 == pout[3]
    assert m.pos3 == pout[4]
    assert m.conj_form == pout[5]
    assert m.conj == pout[6]
    assert m.base == pout[7]
    assert m.yomi == pout[8]
    assert m.pron == pout[9]
