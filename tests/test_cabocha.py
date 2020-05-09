def test_mecab():
    import MeCab

    m = MeCab.Tagger()
    return m


def test_cabocha():
    import CaboCha

    c = CaboCha.Parser()
    return c
