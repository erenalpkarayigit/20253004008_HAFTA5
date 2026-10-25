"""Uzay oyunu dekoratörler modülü.

Bu modül süre ölçme, çağrı sayma, fonksiyon loglama, argüman sınırlama
ve bağımsız bellek önbellekleme dekoratörlerini barındırır.
Tüm dekoratörler fonksiyon imzasını ve meta verilerini korumak için functools.wraps kullanır.
"""

from functools import wraps
import time
from typing import Any, Callable


# ==============================================================================
# Görev 1: Süre Ölçen Dekoratör
# ==============================================================================

def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyonun çalışma süresini time.perf_counter() ile ölçüp yazdıran dekoratör.

    Çıktı biçimi: 'ad: 0.0123 sn'
    Fonksiyonun orijinal sonucunu hiçbir değişiklik yapmadan döndürür.
    __name__ ve __doc__ gibi meta verileri korur.

    Args:
        fonksiyon: Süresi ölçülecek hedef fonksiyon.

    Returns:
        Callable[..., Any]: Sarmalanmış ve süresi ölçülen fonksiyon.
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


# ==============================================================================
# Görev 2: Çağrı Sayacı Dekoratörü
# ==============================================================================

def say(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyonun kaç kez çağrıldığını 'cagri' niteliğinde sayan dekoratör.

    Args:
        fonksiyon: Çağrıları sayılacak fonksiyon.

    Returns:
        Callable[..., Any]: Çağrı sayısını tutan sarmalayıcı fonksiyon.
    """
    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        sarmalayici.cagri += 1
        return fonksiyon(*args, **kwargs)

    sarmalayici.cagri = 0
    return sarmalayici


# ==============================================================================
# Görev 3: Loglayan Dekoratör
# ==============================================================================

def log_cagri(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyon çağrısından önce adı ve argümanlarını, sonrasında dönüş değerini loglayan dekoratör.

    Çıktı formatı:
    -> fonksiyon(arg1, k=v)
    <- fonksiyon = sonuc

    Args:
        fonksiyon: Loglanacak hedef fonksiyon.

    Returns:
        Callable[..., Any]: Çağrısı loglanan sarmalayıcı fonksiyon.
    """
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


# ==============================================================================
# Görev 5: Argüman Alan Sınır Dekoratörü
# ==============================================================================

def sinirla(alt: float, ust: float) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Dekore edilen fonksiyonun ilk argümanının [alt, ust] aralığında olmasını zorunlu kılan dekoratör.

    İlk argüman [alt, ust] aralığı dışında ise ValueError fırlatır:
    'fonksiyon_adi: deger değeri alt-ust aralığında değil'

    Args:
        alt: İzin verilen en küçük değer (sınır dahil).
        ust: İzin verilen en büyük değer (sınır dahil).

    Returns:
        Callable: Fonksiyonu sarmalayan dekoratör.
    """
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
    """Verilen miktarda yakıt harcar ve kalan yakıtı döner (örnek referans yakıt: 100).

    Args:
        miktar: Tüketilecek yakıt miktarı (0 ile 100 arasında olmalıdır).

    Returns:
        int: Harcama sonrası kalan yakıt miktarı (100 - miktar).
    """
    return 100 - miktar


# ==============================================================================
# Bonus: Closure Tabanlı Hafıza (LRU Cache) Dekoratörü
# ==============================================================================

def hafiza(maxsize: int | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """functools.lru_cache kullanmadan closure sözlüğü ile çalışan önbellek dekoratörü.

    maxsize belirtildiğinde önbellek kapasitesi dolunca en eski kullanılan girdiyi (LRU) temizler.

    Args:
        maxsize: Tutulacak en fazla girdi sayısı. None ise sınırsız önbellek tutulur.

    Returns:
        Callable: Fonksiyonu önbellekleyen dekoratör.
    """
    def dekorator(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
        onbellek: dict[Any, Any] = {}

        @wraps(fonksiyon)
        def sarmalayici(*args: Any, **kwargs: Any) -> Any:
            anahtar = (args, tuple(sorted(kwargs.items())))
            if anahtar in onbellek:
                # Erişim olduğunda anahtarı güncel tutmak için sona taşı (LRU)
                deger = onbellek.pop(anahtar)
                onbellek[anahtar] = deger
                return deger

            sonuc = fonksiyon(*args, **kwargs)
            if maxsize is not None and maxsize > 0 and len(onbellek) >= maxsize:
                # En eski elemanı kaldır (FIFO / LRU gereği sözlüğün ilk anahtarı)
                en_eski_anahtar = next(iter(onbellek))
                del onbellek[en_eski_anahtar]

            onbellek[anahtar] = sonuc
            return sonuc

        sarmalayici.onbellek = onbellek
        return sarmalayici

    return dekorator


if __name__ == "__main__":
    import json
    from pathlib import Path

    print("=== Hafta 5 Görev 1: Önbelleksiz Rota Sayacı (adim=20) Süre Ölçümü ===")
    json_yolu = Path(__file__).parent / "galaksi.json"
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

    olculen_rota_sayisi = sure_olc(rota_sayisi_onbelleksiz)
    print("Hesaplanıyor (adim=20)...")
    toplam_rota = olculen_rota_sayisi("dünya", 20)
    print(f"Hesaplanan Rota Sayısı: {toplam_rota}")
