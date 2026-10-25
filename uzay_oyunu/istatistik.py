"""Galaksi istatistikleri ve fonksiyonel programlama araçları modülü.

Bu modül map, filter, reduce ve liste üreteçleri (comprehensions) kullanarak
galaksi verisi üzerinde veri dönüşümleri ve analizler yapar; ayrıca functools.partial
kullanımını örneklendirir.

Okunabilirlik Değerlendirmesi:
------------------------------
Python dünyasında genel kabul görmüş "Pythonic" yaklaşım ve PEP 20 (Zen of Python) ilkeleri
doğrultusunda, Liste Üreteçleri (List Comprehensions) ve yerleşik sum() fonksiyonu;
map(), filter() ve reduce() fonksiyonlarına kıyasla çok daha açık, doğrudan ve okunaklıdır.
- map ve filter ifadelerinde lambda kullanımı ek sözdizimi gürültüsü yaratır ve sonucu
  görüntülemek için ekstra list() dönüşümü gerektirir.
- Liste üreteçlerinde ise dönüştürme ve filtreleme tek bir satırda doğal bir İngilizce
  okuma akışıyla ("x for x in liste if kosul") net biçimde anlaşılır.
- reduce fonksiyonunun okunması diğerlerine göre daha karmaşıktır; bu nedenle Guido van Rossum
  tarafından yerleşik fonksiyonlar arasından çıkarılıp functools modülüne taşınmıştır.
- functools.partial ise bir fonksiyonun belirli parametrelerini sabitleyip yeni bir
  uzmanlaşmış fonksiyon türetmek için son derece temiz, okunaklı ve deklaratif bir yöntemdir.
"""

from functools import partial, reduce
from typing import Any, Callable


# ==============================================================================
# Soru 1: Gezegen Adlarının Büyük Harfli Listesi
# ==============================================================================

def gezegenler_buyuk_harf_map(galaksi: dict[str, Any]) -> list[str]:
    """Gezegen adlarını map() ve lambda kullanarak büyük harflere dönüştürür.

    Args:
        galaksi: Gezegenler listesini barındıran sözlük.

    Returns:
        list[str]: Büyük harflerle yazılmış gezegen isimleri listesi.
    """
    gezegenler: list[str] = galaksi.get("gezegenler", [])
    return list(map(lambda g: g.upper(), gezegenler))


def gezegenler_buyuk_harf_comprehension(galaksi: dict[str, Any]) -> list[str]:
    """Gezegen adlarını liste üreteci (comprehension) kullanarak büyük harflere dönüştürür.

    Args:
        galaksi: Gezegenler listesini barındıran sözlük.

    Returns:
        list[str]: Büyük harflerle yazılmış gezegen isimleri listesi.
    """
    gezegenler: list[str] = galaksi.get("gezegenler", [])
    return [g.upper() for g in gezegenler]


# ==============================================================================
# Soru 2: En Az İki Bağlantısı Olan Gezegenler
# ==============================================================================

def en_az_iki_baglantili_filter(galaksi: dict[str, Any]) -> list[str]:
    """En az iki bağlantısı olan gezegenleri filter() ve lambda kullanarak bulur.

    Args:
        galaksi: Gezegenler ve bağlantılar sözlüğü.

    Returns:
        list[str]: En az 2 bağlantıya sahip gezegenlerin isimleri.
    """
    gezegenler: list[str] = galaksi.get("gezegenler", [])
    baglantilar: dict[str, list[str]] = galaksi.get("baglantilar", {})
    return list(filter(lambda g: len(baglantilar.get(g, [])) >= 2, gezegenler))


def en_az_iki_baglantili_comprehension(galaksi: dict[str, Any]) -> list[str]:
    """En az iki bağlantısı olan gezegenleri liste üreteci kullanarak süzer.

    Args:
        galaksi: Gezegenler ve bağlantılar sözlüğü.

    Returns:
        list[str]: En az 2 bağlantıya sahip gezegenlerin isimleri.
    """
    gezegenler: list[str] = galaksi.get("gezegenler", [])
    baglantilar: dict[str, list[str]] = galaksi.get("baglantilar", {})
    return [g for g in gezegenler if len(baglantilar.get(g, [])) >= 2]


# ==============================================================================
# Soru 3: Toplam Bağlantı Sayısı
# ==============================================================================

def toplam_baglanti_reduce(galaksi: dict[str, Any]) -> int:
    """Toplam gezegen bağlantı sayısını functools.reduce() ile hesaplar.

    Args:
        galaksi: Bağlantılar sözlüğünü içeren galaksi verisi.

    Returns:
        int: Galaksideki toplam yönlü bağlantı sayısı.
    """
    baglantilar: dict[str, list[str]] = galaksi.get("baglantilar", {})
    return reduce(lambda toplam, g: toplam + len(baglantilar.get(g, [])), baglantilar, 0)


def toplam_baglanti_sum(galaksi: dict[str, Any]) -> int:
    """Toplam gezegen bağlantı sayısını yerleşik sum() fonksiyonu ile hesaplar.

    Args:
        galaksi: Bağlantılar sözlüğünü içeren galaksi verisi.

    Returns:
        int: Galaksideki toplam yönlü bağlantı sayısı.
    """
    baglantilar: dict[str, list[str]] = galaksi.get("baglantilar", {})
    return sum(len(komsular) for komsular in baglantilar.values())


# ==============================================================================
# partial ile Hızlı Yolculuk Fonksiyonu
# ==============================================================================

def yolculuk(mesafe: float, hiz: float = 1.0) -> float:
    """Verilen mesafe ve hız değerine göre seyahat süresini hesaplar.

    Args:
        mesafe: Kat edilecek ışık yılı veya birim cinsinden mesafe.
        hiz: Seyahat hızı (warp faktörü / birim).

    Returns:
        float: Yolculuk süresi (mesafe / hiz).

    Raises:
        ValueError: Hız sıfır veya negatifse fırlatılır.
    """
    if hiz <= 0:
        raise ValueError("Hız 0 veya negatif olamaz.")
    return mesafe / hiz


# functools.partial ile hiz=3 sabit türetilmiş hızlı yolculuk fonksiyonu
hizli_yolculuk: Callable[..., float] = partial(yolculuk, hiz=3.0)


if __name__ == "__main__":
    import json
    from pathlib import Path

    json_yolu = Path(__file__).parent / "galaksi.json"
    with open(json_yolu, "r", encoding="utf-8") as f:
        veri = json.load(f)

    print("--- 1. Büyük Harfli Gezegenler ---")
    print("map:", gezegenler_buyuk_harf_map(veri))
    print("comprehension:", gezegenler_buyuk_harf_comprehension(veri))

    print("\n--- 2. En Az İki Bağlantısı Olan Gezegenler ---")
    print("filter:", en_az_iki_baglantili_filter(veri))
    print("comprehension:", en_az_iki_baglantili_comprehension(veri))

    print("\n--- 3. Toplam Bağlantı Sayısı ---")
    print("reduce:", toplam_baglanti_reduce(veri))
    print("sum:", toplam_baglanti_sum(veri))

    print("\n--- 4. functools.partial: hizli_yolculuk ---")
    print("Mesafe 9 için süre (hiz=3):", hizli_yolculuk(9))
