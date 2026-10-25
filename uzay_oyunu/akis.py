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
