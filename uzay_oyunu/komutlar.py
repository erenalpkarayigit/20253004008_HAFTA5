"""Uzay oyunu komut sistemi modülü (Kayıt Deseni / Registry Pattern).

Bu modül komut dekoratörünü, kayıtlı komutlar sözlüğünü (KOMUTLAR)
ve durum tabanlı oyun komutlarını barındırır.
"""

from typing import Any, Callable
from uzay_oyunu.oyun import envanter_metni

# Komut adı -> (fonksiyon, aciklama) haritası
KOMUTLAR: dict[str, tuple[Callable[[dict[str, Any]], str], str]] = {}


def komut(ad: str, aciklama: str = "") -> Callable[[Callable[[dict[str, Any]], str]], Callable[[dict[str, Any]], str]]:
    """Bir fonksiyonu komut sistemine kaydeden dekoratör (Kayıt Deseni).

    Fonksiyonu değiştirmeden (fonksiyon, aciklama) şeklinde KOMUTLAR sözlüğüne kaydeder.
    Aynı komut adı ikinci kez tanımlanmaya çalışılırsa tanım anında ValueError fırlatır.

    Args:
        ad: Komutun çağrılma ismi.
        aciklama: Komutun işlevini açıklayan metin.

    Returns:
        Callable: Orijinal fonksiyonu değiştirmeden döndüren sarmalayıcı/kaydedici.

    Raises:
        ValueError: Komut adı zaten kayıtlıysa fırlatılır.
    """
    def dekorator(fonksiyon: Callable[[dict[str, Any]], str]) -> Callable[[dict[str, Any]], str]:
        if ad in KOMUTLAR:
            raise ValueError(f"Komut zaten kayıtlı: {ad}")
        KOMUTLAR[ad] = (fonksiyon, aciklama)
        return fonksiyon

    return dekorator


@komut("yardim", "komutları listeler")
def yardim(durum: dict[str, Any]) -> str:
    """Tüm kayıtlı komutları ve açıklamalarını alfabetik sırada listeler."""
    satirlar = []
    for k_ad in sorted(KOMUTLAR.keys()):
        _, k_aciklama = KOMUTLAR[k_ad]
        satirlar.append(f"{k_ad} {k_aciklama}")
    return "\n".join(satirlar)


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: dict[str, Any]) -> str:
    """Oyuncunun güncel envanterini gösterir."""
    metin = envanter_metni(
        durum.get("credits", False),
        durum.get("engines", False),
        durum.get("copilot", False),
    )
    return metin if metin else "Envanterde eşya yok."


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: dict[str, Any]) -> str:
    """Bulunulan gezegenden doğrudan ulaşılabilecek gezegenleri virgülle listeler."""
    mevcut = durum.get("konum", "")
    baglantilar = durum.get("baglantilar", {})
    komsular = baglantilar.get(mevcut, [])
    if not komsular:
        return "Gidilebilecek bağlantı yok."
    return ", ".join(komsular)
