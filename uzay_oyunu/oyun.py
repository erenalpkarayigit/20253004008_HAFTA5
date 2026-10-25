"""Uzay oyunu ana modülü.

Bu modül galaksi kurulumunu, envanter ve hedef menüsü gibi saf fonksiyonları
ve uzay yolculuğu (travel) oyun döngüsünü içerir.
"""

import json
from pathlib import Path
from typing import Any

from uzay_oyunu.akis import yakit_gostergesi
from uzay_oyunu.araclar import hamle_sayaci
from uzay_oyunu.dekoratorler import log_cagri


def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """Oyuncunun sahip olduğu eşyaları 'Sende: ...' formatında döndürür.

    Hiçbir eşya yoksa boş string ('') döndürür. Bu fonksiyon saf (pure) bir
    fonksiyondur; ekrana çıktı vermez, yalnızca biçimlendirilmiş metni döner.

    Args:
        credits: Kredi bulunup bulunmadığı durumu.
        engines: Gelişmiş/güçlü motorlar bulunup bulunmadığı durumu.
        copilot: Yardımcı pilot bulunup bulunmadığı durumu.

    Returns:
        str: Sahip olunan eşyaların virgülle ayrılmış metni veya boş string.

    Examples:
        >>> envanter_metni(True, False, True)
        'Sende: bol kredi, yetenekli bir pilot'
        >>> envanter_metni(False, False, False)
        ''
    """
    esyalar: list[str] = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("güçlü motorlar")
    if copilot:
        esyalar.append("yetenekli bir pilot")

    if not esyalar:
        return ""

    return f"Sende: {', '.join(esyalar)}"


@log_cagri
def hedef_menusu(hedefler: list[str]) -> str:
    """Verilen hedef listesini numaralandırarak menü metni olarak döndürür.

    Fonksiyon saf (pure) bir fonksiyondur, log_cagri dekoratörü ile çağrıları loglanır.

    Args:
        hedefler: Gidilebilecek hedef gezegenlerin isim listesi.

    Returns:
        str: Numaralandırılmış hedef seçim menüsü.

    Example:
        >>> print(hedef_menusu(["centauri", "sirius"]))
        Nereye gitmek istersin?
        [1] centauri
        [2] sirius
    """
    satirlar: list[str] = ["Nereye gitmek istersin?"]
    for sira, hedef in enumerate(hedefler, start=1):
        satirlar.append(f"[{sira}] {hedef}")
    return "\n".join(satirlar)


@log_cagri
def galaksi_kur(
    gezegenler: list[str],
    baglantilar: dict[str, list[str]],
    baslangic: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Galaksi haritasını ve başlangıç durumunu oluşturan fonksiyon.

    Args:
        gezegenler: Galaksideki tüm gezegenlerin listesi.
        baglantilar: Gezegenler arası bağlantıları gösteren sözlük.
        baslangic: Oyuna başlanacak gezegen adı.
        **kwargs: Ek parametreler (ör. yakit).

    Returns:
        dict[str, Any]: Galaksi durumunu temsil eden sözlük.

    Raises:
        ValueError: Başlangıç gezegeni gezegenler listesinde yoksa fırlatılır.

    Examples:
        >>> g = galaksi_kur(["mars"], {"mars": []}, "mars")
        >>> g["yakit"]
        50
    """
    if baslangic not in gezegenler:
        raise ValueError(
            f"Başlangıç gezegeni '{baslangic}' gezegenler listesinde bulunamadı."
        )

    yakit = kwargs.get("yakit", 50)

    galaksi: dict[str, Any] = {
        "gezegenler": list(gezegenler),
        "baglantilar": {k: list(v) for k, v in baglantilar.items()},
        "baslangic": baslangic,
        "konum": baslangic,
        "yakit": yakit,
    }

    # kwargs içindeki diğer olası parametreleri de koru
    for anahtar, deger in kwargs.items():
        if anahtar != "yakit":
            galaksi[anahtar] = deger

    return galaksi


def travel(
    galaksi: dict[str, Any] | None = None,
    girdi_saglayici: Any = None,
    tuketim: int = 5,
) -> int:
    """Uzay yolculuğu oyun döngüsünü yürütür.

    Komut sistemini (yardim, envanter, harita) destekler.
    Girdi bir komut adıysa komutu çalıştırıp aynı menüyü tekrar gösterir.
    Girdi sayı ise hedef gezegene seyahat eder.

    Args:
        galaksi: Kullanılacak galaksi verisi. Verilmezse galaksi.json dosyasından yüklenir.
        girdi_saglayici: Testler veya otomatik çalıştırma için girdi fonksiyonu.
        tuketim: Her yolculukta eksilecek yakıt miktarı (varsayılan 5).

    Returns:
        int: Oyunda yapılan toplam hamle sayısı.
    """
    from uzay_oyunu.komutlar import KOMUTLAR

    if galaksi is None:
        json_yolu = Path(__file__).parent / "galaksi.json"
        with open(json_yolu, "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)
        galaksi = galaksi_kur(**veri)

    sayac = hamle_sayaci()
    toplam_hamle = 0

    # Görev 2: Oyunun başında galaksideki yakıt değeriyle bir gösterge üreteci oluştur
    gosterge = yakit_gostergesi(galaksi["yakit"], tuketim)

    has_credits = True
    has_engines = False
    has_copilot = True

    durum = {
        "konum": galaksi["konum"],
        "baglantilar": galaksi["baglantilar"],
        "credits": has_credits,
        "engines": has_engines,
        "copilot": has_copilot,
        "yakit": galaksi["yakit"],
    }

    print("=== Uzay Oyunu Başladı! ===")
    env_str = envanter_metni(has_credits, has_engines, has_copilot)
    if env_str:
        print(env_str)

    input_fn = girdi_saglayici if girdi_saglayici is not None else input

    while True:
        mevcut_konum = galaksi["konum"]
        print(f"\nŞu anki konum: {mevcut_konum} (Kalan Yakıt: {galaksi['yakit']})")

        hedefler = galaksi["baglantilar"].get(mevcut_konum, [])
        if not hedefler:
            print("Gidilecek başka bağlantı kalmadı.")
            break

        print(hedef_menusu(hedefler))

        try:
            secim_raw = input_fn("Seçiminiz: ")
            girdi_temiz = str(secim_raw).strip().lower()

            # Görev 4: Komut kontrolü
            if girdi_temiz in KOMUTLAR:
                komut_fn, _ = KOMUTLAR[girdi_temiz]
                durum["konum"] = galaksi["konum"]
                durum["yakit"] = galaksi["yakit"]
                print(komut_fn(durum))
                continue

            secim_index = int(girdi_temiz) - 1
            if not (0 <= secim_index < len(hedefler)):
                print("Geçersiz seçim, tekrar deneyin.")
                continue
        except (ValueError, EOFError):
            print("Oyun sonlandırıldı.")
            break

        # Görev 2: Her yolculukta göstergeden bir değer çek
        try:
            galaksi["yakit"] = next(gosterge)
        except StopIteration:
            print("Yakıtın bitti, uzayda sürükleniyorsun…")
            break

        hedef_gezegen = hedefler[secim_index]
        galaksi["konum"] = hedef_gezegen
        toplam_hamle = sayac()

        print(f"--> {hedef_gezegen} gezegenine ulaşıldı!")

        if hedef_gezegen == "kara_delik":
            print("Kara deliğe ulaştın! Görev tamamlandı.")
            break

    print(f"Oyunu {toplam_hamle} hamlede bitirdin!")
    return toplam_hamle


if __name__ == "__main__":
    json_dosyasi = Path(__file__).parent / "galaksi.json"
    with open(json_dosyasi, "r", encoding="utf-8") as f:
        galaksi_verisi = json.load(f)

    g = galaksi_kur(**galaksi_verisi)
    print("Galaksi başarıyla kuruldu:", g["konum"], g["yakit"])
