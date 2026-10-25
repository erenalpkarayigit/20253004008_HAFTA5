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


def log_cagri(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyon çağrısından önce adı ve argümanlarını, sonrasında dönüş değerini loglayan dekoratör."""
    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        konumsal = [repr(arg) for arg in args]
        adli = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        tum_argumanlar = ", ".join(konumsal + adli)
        print(f"-> {fonksiyon.__name__}({tum_argumanlar})")
        sonuc = fonksiyon(*args, **kwargs)
        print(f"<- {fonksiyon.__name__} = {repr(sonuc)}")
        return sonuc

    return sarmalayici


def sinirla(alt: float, ust: float) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Dekore edilen fonksiyonun ilk argümanının [alt, ust] aralığında olmasını zorunlu kılan dekoratör."""
    def dekorator(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fonksiyon)
        def sarmalayici(*args: Any, **kwargs: Any) -> Any:
            if not args:
                raise ValueError(f"{fonksiyon.__name__}: En az bir argüman almalıdır.")
            ilk_arg = args[0]
            if ilk_arg < alt or ilk_arg > ust:
                raise ValueError(
                    f"{fonksiyon.__name__}: {ilk_arg} değeri {alt}-{ust} aralığında değil"
                )
            return fonksiyon(*args, **kwargs)
        return sarmalayici
    return dekorator


@sinirla(0, 100)
def yakit_harca(miktar: int) -> int:
    return 100 - miktar
