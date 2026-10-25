from uzay_oyunu.dekoratorler import sure_olc


def test_sure_olc_sonuc_degismeden_donuyor():
    @sure_olc
    def topla(a: int, b: int) -> int:
        return a + b
    assert topla(10, 25) == 35


def test_sure_olc_adli_argumanlarla_cagri():
    @sure_olc
    def selamla(isim: str, unvan: str = "Gezgin") -> str:
        return f"Merhaba {unvan} {isim}"
    assert selamla(isim="Eren", unvan="Kaptan") == "Merhaba Kaptan Eren"
    assert selamla("Eren") == "Merhaba Gezgin Eren"


def test_sure_olc_name_ve_doc_korunuyor():
    @sure_olc
    def ornek_fonksiyon():
        """Bu bir örnek docstring metnidir."""
        return 42
    assert ornek_fonksiyon.__name__ == "ornek_fonksiyon"
    assert ornek_fonksiyon.__doc__ == "Bu bir örnek docstring metnidir."


def test_sure_olc_format(capsys):
    @sure_olc
    def ornek():
        return 1
    ornek()
    out = capsys.readouterr().out
    assert "ornek:" in out
    assert "sn" in out

from functools import lru_cache
from uzay_oyunu.dekoratorler import say


def test_say_yalnizca_fibonacci_21891():
    @say
    def fib1(n: int) -> int:
        if n < 2: return n
        return fib1(n - 1) + fib1(n - 2)
    assert fib1(20) == 6765
    assert fib1.cagri == 21891


def test_say_ustte_lru_altta_39():
    @say
    @lru_cache(maxsize=None)
    def fib2(n: int) -> int:
        if n < 2: return n
        return fib2(n - 1) + fib2(n - 2)
    assert fib2(20) == 6765
    assert fib2.cagri == 39


def test_lru_ustte_say_altta_21():
    @lru_cache(maxsize=None)
    @say
    def fib3(n: int) -> int:
        if n < 2: return n
        return fib3(n - 1) + fib3(n - 2)
    assert fib3(20) == 6765
    assert fib3.__wrapped__.cagri == 21

from uzay_oyunu.dekoratorler import log_cagri


def test_log_cagri_formati(capsys):
    @log_cagri
    def yolculuk(hedef: str, hiz: int = 1) -> str:
        return f"{hedef} hiz={hiz}"
    sonuc = yolculuk("orion", hiz=3)
    assert sonuc == "orion hiz=3"
    cikti = capsys.readouterr().out
    assert "-> yolculuk('orion', hiz=3)" in cikti
    assert "<- yolculuk = 'orion hiz=3'" in cikti
