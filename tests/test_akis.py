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

import pytest
from uzay_oyunu.akis import yakit_gostergesi
from uzay_oyunu.oyun import travel


def test_yakit_gostergesi_ornek_cikti():
    assert list(yakit_gostergesi(100, 30)) == [70, 40, 10, 0]


def test_yakit_gostergesi_stop_iteration():
    g = yakit_gostergesi(50, 25)
    assert next(g) == 25
    assert next(g) == 0
    with pytest.raises(StopIteration):
        next(g)


def test_travel_stop_iteration_yakit_bitti(capsys):
    galaksi = {
        "gezegenler": ["dünya", "centauri"],
        "baglantilar": {"dünya": ["centauri"], "centauri": []},
        "baslangic": "dünya",
        "konum": "dünya",
        "yakit": 10,
    }
    hamleler = iter(["1", "1"])
    travel(galaksi, girdi_saglayici=lambda _: next(hamleler), tuketim=10)
    out = capsys.readouterr().out
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in out

from pathlib import Path
from uzay_oyunu.akis import satirlari_oku, ayristir, uzun_yolculuklar
import inspect


def test_seyir_defteri_boru_hatti():
    yol = Path(__file__).parent.parent / "veri" / "seyir.txt"
    assert sum(y for _, _, y in ayristir(satirlari_oku(yol))) == 88
    kayitlar = ayristir(satirlari_oku(yol))
    assert [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)] == ["sirius", "centauri", "orion", "kara_delik"]
    assert inspect.isgenerator(satirlari_oku(yol))
