"""Uzay oyunu akış ve üreteçler modülü."""

from collections.abc import Generator


def fibonacci() -> Generator[int, None, None]:
    """Sonsuz Fibonacci sayı dizisi üreteci.

    0 ve 1 ile başlayarak her adımda bir sonraki Fibonacci sayısını üretir.
    Üreteç tek kullanımlıktır; tüketildikçe durumunu ilerletir.

    Yields:
        int: Sıradaki Fibonacci sayısı.
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def yakit_gostergesi(yakit: int, tuketim: int) -> Generator[int, None, None]:
    """Her next() çağrısında yakıtı tüketim kadar azaltıp kalan yakıtı üreten üreteç.

    Yakıt 0'a inince durur (StopIteration fırlatır).
    """
    kalan = yakit
    while kalan > 0:
        kalan = max(0, kalan - tuketim)
        yield kalan

from pathlib import Path
from collections.abc import Iterable


def satirlari_oku(yol: str | Path) -> Generator[str, None, None]:
    """Dosyayı satır satır okuyarak boş ve '#' ile başlayan satırları atlayan üreteç."""
    with open(yol, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            temiz = satir.strip()
            if not temiz or temiz.startswith("#"):
                continue
            yield temiz


def ayristir(satirlar: Iterable[str]) -> Generator[tuple[str, str, int], None, None]:
    """'kaynak -> hedef yakit' formatındaki satırlardan (kaynak, hedef, yakit) demeti üretir."""
    for satir in satirlar:
        if "->" in satir:
            kaynak, hedef_yakit = satir.split("->", 1)
            hedef, yakit_str = hedef_yakit.strip().rsplit(None, 1)
            yield (kaynak.strip(), hedef.strip(), int(yakit_str))


def uzun_yolculuklar(kayitlar: Iterable[tuple[str, str, int]], esik: int) -> Generator[tuple[str, str, int], None, None]:
    """Yakıt miktarı verilen eşikten büyük olan kayıtları süzen üreteç."""
    for kayit in kayitlar:
        if kayit[2] > esik:
            yield kayit
