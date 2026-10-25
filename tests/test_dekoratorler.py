"""Hafta 5: Dekoratörler birim testleri.

Görev 1 (sure_olc), Görev 2 (say ve dekoratör sırası), Görev 3 (log_cagri),
Görev 4 (komut sistemi kayıt deseni), Görev 5 (sinirla) ve Bonus (hafiza)
testlerini içerir.
"""

from functools import lru_cache
import json
from pathlib import Path
import pytest

from uzay_oyunu.dekoratorler import (
    sure_olc,
    say,
    log_cagri,
    sinirla,
    yakit_harca,
    hafiza,
)
from uzay_oyunu.komutlar import KOMUTLAR, komut, yardim, envanter, harita
from uzay_oyunu.oyun import galaksi_kur, hedef_menusu, travel


# ==============================================================================
# Görev 1 Testleri – Süre Ölçen Dekoratör (15 Puan)
# ==============================================================================

def test_sure_olc_sonuc_degismeden_donuyor():
    """Fonksiyonun dönüş değerinin değişmeden döndüğünü test eder."""
    @sure_olc
    def topla(a: int, b: int) -> int:
        return a + b

    assert topla(10, 25) == 35


def test_sure_olc_adli_argumanlarla_cagri():
    """Adlı (keyword) argümanlarla yapılan çağrıların çalıştığını test eder."""
    @sure_olc
    def selamla(isim: str, unvan: str = "Gezgin") -> str:
        return f"Merhaba {unvan} {isim}"

    assert selamla(isim="Eren", unvan="Kaptan") == "Merhaba Kaptan Eren"
    assert selamla("Eren") == "Merhaba Gezgin Eren"


def test_sure_olc_name_ve_doc_korunuyor():
    """__name__ ve __doc__ meta verilerinin functools.wraps ile korunduğunu test eder."""
    @sure_olc
    def ornek_fonksiyon():
        """Bu bir örnek docstring metnidir."""
        return 42

    assert ornek_fonksiyon.__name__ == "ornek_fonksiyon"
    assert ornek_fonksiyon.__doc__ == "Bu bir örnek docstring metnidir."


def test_sure_olc_format_ve_hafta4_rota_sayaci(capsys):
    """Hafta 4'teki önbelleksiz rota sayacına uygulanıp çıktının 'ad: 0.0123 sn' biçiminde olduğunu test eder."""
    baglantilar = {
        "dünya": ["centauri", "sirius"],
        "centauri": ["dünya", "orion"],
        "sirius": ["dünya", "centauri"],
        "orion": ["dünya"],
    }

    def rota_sayisi_onbelleksiz(gezegen: str, adim: int) -> int:
        if adim == 0:
            return 1
        return sum(rota_sayisi_onbelleksiz(komsu, adim - 1) for komsu in baglantilar.get(gezegen, []))

    olculen = sure_olc(rota_sayisi_onbelleksiz)
    sonuc = olculen("dünya", 5)
    assert sonuc > 0

    yakalanan = capsys.readouterr().out
    assert "rota_sayisi_onbelleksiz:" in yakalanan
    assert "sn" in yakalanan


def test_sure_olc_hafta4_rota_sayaci_adim_20(capsys):
    """Hafta 4'teki önbelleksiz rota sayacına uygulanıp adim=20 için süreyi gösterir."""
    json_yolu = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"
    with open(json_yolu, "r", encoding="utf-8") as f:
        galaksi = json.load(f)
    baglantilar = galaksi["baglantilar"]

    def rota_sayisi_onbelleksiz(gezegen: str, adim: int) -> int:
        if adim == 0:
            return 1
        return sum(
            rota_sayisi_onbelleksiz(komsu, adim - 1)
            for komsu in baglantilar.get(gezegen, [])
        )

    olculen = sure_olc(rota_sayisi_onbelleksiz)
    sonuc = olculen("dünya", 20)
    assert sonuc == 4315343

    yakalanan = capsys.readouterr().out
    assert "rota_sayisi_onbelleksiz:" in yakalanan
    assert "sn" in yakalanan


# ==============================================================================
# Görev 2 Testleri – Çağrı Sayacı ve Dekoratör Sırası (20 Puan)
# ==============================================================================

def test_say_yalnizca_fibonacci_21891():
    """Yalnızca @say ile süslenmiş fib(20) çağrı sayısının tam 21891 olduğunu doğrular."""
    @say
    def fib1(n: int) -> int:
        if n < 2:
            return n
        return fib1(n - 1) + fib1(n - 2)

    sonuc = fib1(20)
    assert sonuc == 6765
    assert fib1.cagri == 21891


def test_say_ustte_lru_altta_39():
    """@say üstte, @lru_cache altta iken fib(20) çağrı sayısının tam 39 olduğunu doğrular."""
    @say
    @lru_cache(maxsize=None)
    def fib2(n: int) -> int:
        if n < 2:
            return n
        return fib2(n - 1) + fib2(n - 2)

    sonuc = fib2(20)
    assert sonuc == 6765
    assert fib2.cagri == 39


def test_lru_ustte_say_altta_21():
    """@lru_cache üstte, @say altta iken fib.__wrapped__.cagri değerinin tam 21 olduğunu doğrular."""
    @lru_cache(maxsize=None)
    @say
    def fib3(n: int) -> int:
        if n < 2:
            return n
        return fib3(n - 1) + fib3(n - 2)

    sonuc = fib3(20)
    assert sonuc == 6765
    assert fib3.__wrapped__.cagri == 21


# ==============================================================================
# Görev 3 Testleri – Loglayan Dekoratör (15 Puan)
# ==============================================================================

def test_log_cagri_formati(capsys):
    """log_cagri dekoratörünün '-> fn(...) ' ve '<- fn = ...' formatında yazdırdığını test eder."""
    @log_cagri
    def yolculuk(hedef: str, hiz: int = 1) -> str:
        return f"{hedef} hiz={hiz}"

    sonuc = yolculuk("orion", hiz=3)
    assert sonuc == "orion hiz=3"

    cikti = capsys.readouterr().out
    assert "-> yolculuk('orion', hiz=3)" in cikti
    assert "<- yolculuk = 'orion hiz=3'" in cikti


def test_galaksi_kur_ve_hedef_menusu_log_cagri_ile_calisir():
    """log_cagri ile dekore edilmiş galaksi_kur ve hedef_menusu fonksiyonlarının doğru çalıştığını test eder."""
    g = galaksi_kur(["dünya", "mars"], {"dünya": ["mars"], "mars": []}, "dünya")
    assert g["konum"] == "dünya"

    menu = hedef_menusu(["mars"])
    assert "[1] mars" in menu


# ==============================================================================
# Görev 4 Testleri – Komut Sistemi (30 Puan)
# ==============================================================================

def test_komut_kayit_ve_ayni_ad_hatasi():
    """Komutların KOMUTLAR sözlüğüne kaydedildiğini ve aynı adın tekrarında ValueError fırlattığını test eder."""
    assert "yardim" in KOMUTLAR
    assert "envanter" in KOMUTLAR
    assert "harita" in KOMUTLAR

    with pytest.raises(ValueError, match="Komut zaten kayıtlı: yardim"):
        @komut("yardim", "tekrar deneme")
        def sahte_yardim(durum):
            return ""


def test_yardim_komutu():
    """yardim komutunun tüm komutları alfabetik sırada listelediğini test eder."""
    durum = {}
    cikti = yardim(durum)
    satirlar = cikti.splitlines()
    assert len(satirlar) >= 3
    assert "envanter eşyalarını gösterir" in cikti
    assert "harita gidebileceğin gezegenleri gösterir" in cikti
    assert "yardim komutları listeler" in cikti


def test_envanter_komutu():
    """envanter komutunun oyuncunun durumundaki eşyaları doğru yansıttığını test eder."""
    durum_dolu = {"credits": True, "engines": False, "copilot": True}
    assert envanter(durum_dolu) == "Sende: bol kredi, yetenekli bir pilot"

    durum_bos = {"credits": False, "engines": False, "copilot": False}
    assert envanter(durum_bos) == "Envanterde eşya yok."


def test_harita_komutu():
    """harita komutunun mevcut konumdaki bağlantıları virgülle listelediğini test eder."""
    durum = {
        "konum": "dünya",
        "baglantilar": {"dünya": ["centauri", "sirius"]},
    }
    assert harita(durum) == "centauri, sirius"


def test_travel_icinde_komut_calistirma(capsys):
    """travel() döngüsünde komut girildiğinde komutun çalışıp menünün tekrar gösterildiğini test eder."""
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
    # Sırasıyla 'harita' komutu, 'yardim' komutu ve ardından '1' seçimi (centauri), sonra '1' seçimi (kara_delik)
    girdiler = iter(["harita", "yardim", "1", "1"])
    toplam_hamle = travel(galaksi, girdi_saglayici=lambda _: next(girdiler))

    cikti = capsys.readouterr().out
    assert "centauri" in cikti  # harita komutu çıktısı
    assert "yardim komutları listeler" in cikti  # yardim komutu çıktısı
    assert toplam_hamle == 2


# ==============================================================================
# Görev 5 Testleri – Argüman Alan Sınır Dekoratörü (20 Puan)
# ==============================================================================

def test_yakit_harca_gecerli_degerler():
    """yakit_harca fonksiyonunun 0, 30 ve 100 için doğru çalıştığını test eder."""
    assert yakit_harca(30) == 70
    assert yakit_harca(0) == 100
    assert yakit_harca(100) == 0


def test_yakit_harca_aralik_disi_hatalar():
    """yakit_harca fonksiyonunun aralık dışı değerlerde ValueError fırlattığını test eder."""
    with pytest.raises(ValueError, match="yakit_harca: 150 değeri 0-100 aralığında değil"):
        yakit_harca(150)

    with pytest.raises(ValueError, match="yakit_harca: -1 değeri 0-100 aralığında değil"):
        yakit_harca(-1)

    with pytest.raises(ValueError, match="yakit_harca: 101 değeri 0-100 aralığında değil"):
        yakit_harca(101)


def test_sinirla_ozel_fonksiyon():
    """sinirla dekoratörünün farklı aralıklarda da başarıyla çalıştığını test eder."""
    @sinirla(10, 50)
    def motor_gucu(guc: int) -> int:
        return guc * 2

    assert motor_gucu(10) == 20
    assert motor_gucu(50) == 100

    with pytest.raises(ValueError, match="motor_gucu: 5 değeri 10-50 aralığında değil"):
        motor_gucu(5)


# ==============================================================================
# Bonus Testleri – hafiza (Closure Tabanlı LRU Cache) (+10 Puan)
# ==============================================================================

def test_hafiza_onbellekleme():
    """hafiza dekoratörünün sonuçları önbelleğe alıp tekrar çalıştırmadığını test eder."""
    cagri_sayisi = 0

    @hafiza()
    def kare(x: int) -> int:
        nonlocal cagri_sayisi
        cagri_sayisi += 1
        return x * x

    assert kare(4) == 16
    assert cagri_sayisi == 1
    assert kare(4) == 16
    assert cagri_sayisi == 1  # İkinci çağrıda fonksiyon çalıştırılmadı


def test_hafiza_maxsize_tahliyesi():
    """maxsize dolduğunda en eski kullanılan girdinin önbellekten silindiğini test eder."""
    cagri_sayisi = 0

    @hafiza(maxsize=2)
    def kup(x: int) -> int:
        nonlocal cagri_sayisi
        cagri_sayisi += 1
        return x ** 3

    kup(1)  # cache: {1: 1}
    kup(2)  # cache: {1: 1, 2: 8}
    assert cagri_sayisi == 2

    kup(3)  # cache doldu, en eski (1) silinir, {2: 8, 3: 27}
    assert cagri_sayisi == 3

    # 2 hala önbellekte olmalı:
    assert kup(2) == 8
    assert cagri_sayisi == 3

    # 1 silinmiş olmalı, tekrar hesaplanmalı:
    assert kup(1) == 1
    assert cagri_sayisi == 4


def test_hafiza_ile_lru_cache_karsilastirma():
    """hafiza ve functools.lru_cache dekoratörlerinin aynı sonuçları ürettiğini test eder."""
    @hafiza(maxsize=128)
    def fib_hafiza(n: int) -> int:
        if n < 2:
            return n
        return fib_hafiza(n - 1) + fib_hafiza(n - 2)

    @lru_cache(maxsize=128)
    def fib_builtin(n: int) -> int:
        if n < 2:
            return n
        return fib_builtin(n - 1) + fib_builtin(n - 2)

    for i in range(25):
        assert fib_hafiza(i) == fib_builtin(i)
