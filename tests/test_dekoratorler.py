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
