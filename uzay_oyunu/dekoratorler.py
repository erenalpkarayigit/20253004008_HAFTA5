"""Uzay oyunu dekoratörler modülü."""

from functools import wraps
import time
from typing import Any, Callable


def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyonun çalışma süresini time.perf_counter() ile ölçüp yazdıran dekoratör.

    Çıktı biçimi: 'ad: 0.0123 sn'
    """
    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        bitis = time.perf_counter()
        gecen = bitis - baslangic
        print(f"{fonksiyon.__name__}: {gecen:.4f} sn")
        return sonuc

    return sarmalayici


def say(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyonun kaç kez çağrıldığını 'cagri' niteliğinde sayan dekoratör."""
    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        sarmalayici.cagri += 1
        return fonksiyon(*args, **kwargs)

    sarmalayici.cagri = 0
    return sarmalayici
