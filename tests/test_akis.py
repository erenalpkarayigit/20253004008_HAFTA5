"""Hafta 4: Üreteçler ve functools birim testleri.

Görev 1 (Fibonacci), Görev 2 (Yakıt Göstergesi), Görev 3 (Seyir Defteri Boru Hattı),
Görev 4 (Önbellekli Rota Sayacı), Görev 5 (İstatistik ve partial) ve Bonus (Zamanlayıcı)
testlerini içerir.
"""

from collections.abc import Generator
import inspect
from itertools import islice, takewhile
import json
from pathlib import Path

import pytest

from uzay_oyunu.akis import (
    fibonacci,
    yakit_gostergesi,
    satirlari_oku,
    ayristir,
    uzun_yolculuklar,
    rota_sayaci,
    zamanlayici,
    zamanlayici_programi,
)
from uzay_oyunu.oyun import travel, galaksi_kur
from uzay_oyunu.istatistik import (
    gezegenler_buyuk_harf_map,
    gezegenler_buyuk_harf_comprehension,
    en_az_iki_baglantili_filter,
    en_az_iki_baglantili_comprehension,
    toplam_baglanti_reduce,
    toplam_baglanti_sum,
    yolculuk,
    hizli_yolculuk,
)


# ==============================================================================
# Görev 1 Testleri – Fibonacci Üreteci (15 Puan)
# ==============================================================================

def test_fibonacci_next_uc_deger():
    """next() ile ilk 3 değerin (0, 1, 1) geldiğini doğrular."""
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice_oniki():
    """itertools.islice ile ilk 12 Fibonacci sayısının doğruluğunu test eder."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert list(islice(fibonacci(), 12)) == beklenen


def test_fibonacci_takewhile_yuzden_kucuk():
    """itertools.takewhile ile 100'den küçük Fibonacci sayılarını test eder."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    sonuc = list(takewhile(lambda x: x < 100, fibonacci()))
    assert sonuc == beklenen


def test_fibonacci_tek_kullanimlik():
    """Aynı üreteç nesnesinden ikinci çağrının farklı sonuç verdiğini (tüketildiğini) gösterir."""
    g = fibonacci()
    ilk_bes = list(islice(g, 5))
    ikinci_bes = list(islice(g, 5))

    assert ilk_bes == [0, 1, 1, 2, 3]
    assert ikinci_bes == [5, 8, 13, 21, 34]
    assert ilk_bes != ikinci_bes


# ==============================================================================
# Görev 2 Testleri – Yakıt Göstergesi (20 Puan)
# ==============================================================================

def test_yakit_gostergesi_ornek_cikti():
    """Ödev metnindeki list(yakit_gostergesi(100, 30)) çıktısını doğrular."""
    assert list(yakit_gostergesi(100, 30)) == [70, 40, 10, 0]


def test_yakit_gostergesi_stop_iteration():
    """Yakıt 0'a ulaştığında StopIteration fırlatıldığını doğrular."""
    g = yakit_gostergesi(50, 25)
    assert next(g) == 25
    assert next(g) == 0
    with pytest.raises(StopIteration):
        next(g)


def test_travel_stop_iteration_yakit_bitti(capsys):
    """travel() içinde yakıt tükendiğinde StopIteration yakalanarak oyunun sonlandığını test eder."""
    galaksi = {
        "gezegenler": ["dünya", "centauri", "orion", "kara_delik"],
        "baglantilar": {
            "dünya": ["centauri"],
            "centauri": ["orion"],
            "orion": ["kara_delik"],
            "kara_delik": [],
        },
        "baslangic": "dünya",
        "konum": "dünya",
        "yakit": 10,
    }
    # Her adımda 10 yakıt tüketilsin; ilk adımda yakıt 0 olur, ikinci adımda StopIteration fırlatılır
    hamleler = iter(["1", "1", "1"])
    toplam_hamle = travel(galaksi, girdi_saglayici=lambda _: next(hamleler), tuketim=10)

    yakalanan = capsys.readouterr().out
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in yakalanan
    assert toplam_hamle == 1


def test_travel_kara_delik_basarili(capsys):
    """Yeterli yakıt olduğunda hedefe ulaşılabildiğini doğrular."""
    galaksi = {
        "gezegenler": ["dünya", "centauri", "kara_delik"],
        "baglantilar": {
            "dünya": ["centauri"],
            "centauri": ["kara_delik"],
            "kara_delik": [],
        },
        "baslangic": "dünya",
        "konum": "dünya",
        "yakit": 100,
    }
    hamleler = iter(["1", "1"])
    toplam_hamle = travel(galaksi, girdi_saglayici=lambda _: next(hamleler), tuketim=5)

    yakalanan = capsys.readouterr().out
    assert "Kara deliğe ulaştın! Görev tamamlandı." in yakalanan
    assert toplam_hamle == 2


# ==============================================================================
# Görev 3 Testleri – Seyir Defteri Boru Hattı (25 Puan)
# ==============================================================================

@pytest.fixture
def seyir_dosyasi_yolu() -> Path:
    """Projedeki veri/seyir.txt dosya yolunu döner."""
    yol = Path(__file__).parent.parent / "veri" / "seyir.txt"
    assert yol.exists(), f"{yol} dosyası bulunamadı!"
    return yol


def test_satirlari_oku(seyir_dosyasi_yolu):
    """Boş ve '#' ile başlayan satırların atlandığını test eder."""
    satirlar = list(satirlari_oku(seyir_dosyasi_yolu))
    assert len(satirlar) == 6
    assert all(not s.startswith("#") for s in satirlar)
    assert all(len(s) > 0 for s in satirlar)


def test_ayristir_ve_toplam_yakit(seyir_dosyasi_yolu):
    """Ödevdeki sum(y for _, _, y in ayristir(satirlari_oku(...))) == 88 çıktısını test eder."""
    toplam = sum(y for _, _, y in ayristir(satirlari_oku(seyir_dosyasi_yolu)))
    assert toplam == 88


def test_uzun_yolculuklar(seyir_dosyasi_yolu):
    """Ödevdeki [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)] çıktısını test eder."""
    kayitlar = ayristir(satirlari_oku(seyir_dosyasi_yolu))
    hedefler = [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)]
    assert hedefler == ["sirius", "centauri", "orion", "kara_delik"]


def test_boru_hatti_tembellik(seyir_dosyasi_yolu):
    """Hiçbir fonksiyonun tüm veriyi listeye okumadığını, üreteç döndürdüğünü test eder."""
    g1 = satirlari_oku(seyir_dosyasi_yolu)
    assert inspect.isgenerator(g1)

    g2 = ayristir(g1)
    assert inspect.isgenerator(g2)

    g3 = uzun_yolculuklar(g2, 10)
    assert inspect.isgenerator(g3)


# ==============================================================================
# Görev 4 Testleri – Önbellekli Rota Sayacı (25 Puan)
# ==============================================================================

@pytest.fixture
def galaksi_verisi() -> dict:
    """uzay_oyunu/galaksi.json dosyasından galaksi verisini yükler."""
    json_yolu = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"
    with open(json_yolu, "r", encoding="utf-8") as f:
        return json.load(f)


def test_rota_sayaci_ornek_degerler(galaksi_verisi):
    """say('dünya', 3) == 9, say('dünya', 10) == 2185, say('dünya', 40) == 16832258606399."""
    say = rota_sayaci(galaksi_verisi["baglantilar"])
    assert say("dünya", 3) == 9
    assert say("dünya", 10) == 2185
    assert say("dünya", 40) == 16832258606399


def test_rota_sayaci_adim_sifir(galaksi_verisi):
    """0 adımda başlangıç gezegeninde bulunma durumunun 1 olduğunu test eder."""
    say = rota_sayaci(galaksi_verisi["baglantilar"])
    for gezegen in galaksi_verisi["gezegenler"]:
        assert say(gezegen, 0) == 1


def test_rota_sayaci_lru_cache_bilgisi(galaksi_verisi):
    """@lru_cache dekoratörünün önbellek isabeti (hits) ürettiğini doğrular."""
    say = rota_sayaci(galaksi_verisi["baglantilar"])
    say("dünya", 20)
    info = say.cache_info()
    assert info.hits > 0
    assert info.currsize > 0


# ==============================================================================
# Görev 5 Testleri – map, filter, reduce ve partial (15 Puan)
# ==============================================================================

def test_gezegenler_buyuk_harf_iki_yol(galaksi_verisi):
    """Gezegen adlarının büyük harfli listesini hem map hem comprehension ile test eder."""
    beklenen = ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]
    sonuc_map = gezegenler_buyuk_harf_map(galaksi_verisi)
    sonuc_comp = gezegenler_buyuk_harf_comprehension(galaksi_verisi)

    assert sonuc_map == beklenen
    assert sonuc_comp == beklenen


def test_en_az_iki_baglantili_iki_yol(galaksi_verisi):
    """En az 2 bağlantısı olan gezegenleri hem filter hem comprehension ile test eder."""
    beklenen = ["dünya", "centauri", "sirius", "orion"]
    sonuc_filter = en_az_iki_baglantili_filter(galaksi_verisi)
    sonuc_comp = en_az_iki_baglantili_comprehension(galaksi_verisi)

    assert sonuc_filter == beklenen
    assert sonuc_comp == beklenen


def test_toplam_baglanti_iki_yol(galaksi_verisi):
    """Toplam bağlantı sayısını (10) hem reduce hem sum ile test eder."""
    sonuc_reduce = toplam_baglanti_reduce(galaksi_verisi)
    sonuc_sum = toplam_baglanti_sum(galaksi_verisi)

    assert sonuc_reduce == 10
    assert sonuc_sum == 10


def test_hizli_yolculuk_partial():
    """functools.partial ile türetilen hizli_yolculuk (hiz=3) fonksiyonunu test eder."""
    assert yolculuk(30, 2) == 15.0
    assert hizli_yolculuk(9) == 3.0
    assert hizli_yolculuk(30) == 10.0

    with pytest.raises(ValueError):
        yolculuk(10, 0)


# ==============================================================================
# Bonus Testleri – zamanlayici (Meşgul Bekleme) (+10 Puan)
# ==============================================================================

def test_zamanlayici_uretec():
    """zamanlayici'nın bir üreteç olduğunu ve zaman aralığı dolduğunda True ürettiğini test eder."""
    z = zamanlayici(0.001)
    assert inspect.isgenerator(z)

    # Bir süre çağrıldığında True üretmelidir
    dongu_sayisi = 0
    tetiklendi = False
    while dongu_sayisi < 100000:
        if next(z):
            tetiklendi = True
            break
        dongu_sayisi += 1

    assert tetiklendi, "Zamanlayıcı beklenen süre içinde True üretmedi."


def test_zamanlayici_programi_kisa():
    """zamanlayici_programi fonksiyonunun kısa süreli çalışmasını test eder."""
    olaylar = zamanlayici_programi(toplam_sure=0.05, yazdir=False)
    assert isinstance(olaylar, list)
