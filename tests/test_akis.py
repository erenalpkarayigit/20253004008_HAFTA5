from itertools import islice, takewhile
from uzay_oyunu.akis import fibonacci


def test_fibonacci_next_uc_deger():
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice_oniki():
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert list(islice(fibonacci(), 12)) == beklenen


def test_fibonacci_takewhile_yuzden_kucuk():
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    sonuc = list(takewhile(lambda x: x < 100, fibonacci()))
    assert sonuc == beklenen


def test_fibonacci_tek_kullanimlik():
    g = fibonacci()
    ilk_bes = list(islice(g, 5))
    ikinci_bes = list(islice(g, 5))
    assert ilk_bes == [0, 1, 1, 2, 3]
    assert ikinci_bes == [5, 8, 13, 21, 34]
    assert ilk_bes != ikinci_bes
