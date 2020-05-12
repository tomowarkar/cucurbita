import pytest

from cucurbita.cab import Chunk

header1 = "* 0 2D 0/1 -1.911675"
morphs1 = ["surface\tpos,pos1,pos2,pos3,conj_form,conj,base,yomi,pron"]


@pytest.mark.parametrize(
    "pin, pout", [((header1, morphs1), 0)],
)
def test_chunk_default_pos(pin, pout):
    c = Chunk(morphs=pin[1], header=pin[0])
    assert c.pos == pout


@pytest.mark.parametrize(
    "pin, pout", [((header1, morphs1), 2)],
)
def test_chunk_default_dst(pin, pout):
    c = Chunk(morphs=pin[1], header=pin[0])
    assert c.dst == pout


@pytest.mark.parametrize(
    "pin, pout", [((header1, morphs1), -1.911675)],
)
def test_chunk_default_score(pin, pout):
    c = Chunk(morphs=pin[1], header=pin[0])
    assert c.score == pout
