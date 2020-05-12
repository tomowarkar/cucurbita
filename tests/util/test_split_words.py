import pytest

from cucurbita.util import split_words

morph1 = "surface\tpos,pos1,pos2,pos3,conj_form,conj,base,yomi,pron"
expect1 = [
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
morph2 = "surface\tpos,pos1,pos2,pos3,conj_form,conj,base"
expect2 = [
    "surface",
    "pos",
    "pos1",
    "pos2",
    "pos3",
    "conj_form",
    "conj",
    "base",
    None,
    None,
]


@pytest.mark.parametrize(
    "pin, pout", [(morph1, expect1), (morph1 + "\n", expect1)],
)
def test_sw_default(pin, pout):
    assert split_words(pin) == pout


@pytest.mark.parametrize(
    "pin, pout", [(morph2, expect2), (morph2 + "\n", expect2)],
)
def test_sw_less_words(pin, pout):
    assert split_words(pin) == pout
