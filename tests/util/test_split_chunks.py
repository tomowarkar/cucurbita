from cucurbita.util import split_chunks


def test_sc_cabocha_default():
    sentence = "隣\t名詞,一般,*,*,*,*,隣,トナリ,トナリ\nの\t助詞,連体化,*,*,*,*,の,ノ,ノ\n客\t名詞,一般,*,*,*,*,客,キャク,キャク\nは\t助詞,係助詞,*,*,*,*,は,ハ,ワ\nよく\t副詞,一般,*,*,*,*,よく,ヨク,ヨク\n柿\t名詞,一般,*,*,*,*,柿,カキ,カキ\n食う\t動詞,自立,*,*,五段・ワ行促音便,基本形,食う,クウ,クウ\n客\t名詞,一般,*,*,*,*,客,キャク,キャク\nだ\t助動詞,*,*,*,特殊・ダ,基本形,だ,ダ,ダ\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n"
    chunks = [e for e in split_chunks(sentence)]

    assert len(chunks) == 1, "Invalid output length: mecabの解析結果は文節情報がないので出力は1である"
    assert [chunk for chunk in chunks if chunk[0] != ""] == [], "ヘッダーは空文字"
    assert [chunk for chunk in chunks if chunk[1] == ""] == [], "形態素解析結果を含む"
    assert [chunk for chunk in chunks if len(chunk) != 2] == [], "header と morphsを返す"
    assert len(chunks[0][1]) == 10, "Invalid morph length: 単語の数と一致"
    assert (
        chunks[0][1][0] == "隣\t名詞,一般,*,*,*,*,隣,トナリ,トナリ"
    ), "Invalid output morph shape: 改行のない単語形態素解析結果を返す"


def test_sc_mecab_default():
    sentence_mecab = "* 0 1D 0/1 2.206035\n隣\t名詞,一般,*,*,*,*,隣,トナリ,トナリ\nの\t助詞,連体化,*,*,*,*,の,ノ,ノ\n* 1 5D 0/1 -0.593304\n客\t名詞,一般,*,*,*,*,客,キャク,キャク\nは\t助詞,係助詞,*,*,*,*,は,ハ,ワ\n* 2 4D 0/0 0.538813\nよく\t副詞,一般,*,*,*,*,よく,ヨク,ヨク\n* 3 4D 0/0 1.985106\n柿\t名詞,一般,*,*,*,*,柿,カキ,カキ\n* 4 5D 0/0 -0.593304\n食う\t動詞,自立,*,*,五段・ワ行促音便,基本形,食う,クウ,クウ\n* 5 -1D 0/1 0.000000\n客\t名詞,一般,*,*,*,*,客,キャク,キャク\nだ\t助動詞,*,*,*,特殊・ダ,基本形,だ,ダ,ダ\n。\t記号,句点,*,*,*,*,。,。,。\nEOS\n"
    chunks = [e for e in split_chunks(sentence_mecab)]

    assert len(chunks) == 6, "Invalid output length: headerの数と一致"
    assert [chunk for chunk in chunks if chunk[0] == ""] == [], "ヘッダーは空文字でない"
    assert [chunk for chunk in chunks if chunk[1] == ""] == [], "形態素解析結果を含む"
    assert [chunk for chunk in chunks if len(chunk) != 2] == [], "header と morphsを返す"
    assert chunks[0] == (
        "* 0 1D 0/1 2.206035",
        ["隣\t名詞,一般,*,*,*,*,隣,トナリ,トナリ", "の\t助詞,連体化,*,*,*,*,の,ノ,ノ"],
    ), "Invalid data: header情報と単語解析結果の配列を返す"
    assert len(chunks[0][1]) == 2, "Invalid morph length: 単語の数と一致"
    assert (
        chunks[0][1][0] == "隣\t名詞,一般,*,*,*,*,隣,トナリ,トナリ"
    ), "Invalid output morph shape: 改行のない単語形態素解析結果を返す"


def test_sc_blank():
    sentence = ""
    chunks = [e for e in split_chunks(sentence)]
    assert chunks == [("", [])], "Invalid output data"
