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
