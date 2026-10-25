"""Uzay oyunu akış ve üreteçler modülü.

Bu modül Fibonacci üreteci, yakıt göstergesi, seyir defteri veri boru hattı,
önbellekli rota sayacı ve zamanlayıcı üreteçlerini içerir.
"""

from collections.abc import Generator, Iterable
from functools import lru_cache
from pathlib import Path
import time
from typing import Callable


def fibonacci() -> Generator[int, None, None]:
    """Sonsuz Fibonacci sayı dizisi üreteci.

    0 ve 1 ile başlayarak her adımda bir sonraki Fibonacci sayısını üretir.
    Üreteç tek kullanımlıktır; tüketildikçe durumunu ilerletir.

    Yields:
        int: Sıradaki Fibonacci sayısı.

    Examples:
        >>> g = fibonacci(); next(g), next(g), next(g)
        (0, 1, 1)
        >>> from itertools import islice
        >>> list(islice(fibonacci(), 12))
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def yakit_gostergesi(yakit: int, tuketim: int) -> Generator[int, None, None]:
    """Her next() çağrısında yakıtı tüketim kadar azaltıp kalan yakıtı üreten üreteç.

    Yakıt 0'a inince durur (StopIteration fırlatır).

    Args:
        yakit: Başlangıç yakıt seviyesi.
        tuketim: Her adımda eksilecek yakıt miktarı.

    Yields:
        int: Kalan yakıt miktarı (0 dahil).

    Example:
        >>> list(yakit_gostergesi(100, 30))
        [70, 40, 10, 0]
    """
    kalan = yakit
    while kalan > 0:
        kalan = max(0, kalan - tuketim)
        yield kalan


def satirlari_oku(yol: str | Path) -> Generator[str, None, None]:
    """Dosyayı satır satır okuyarak boş ve '#' ile başlayan satırları atlayan üreteç.

    Tüm dosyayı bir kerede belleğe okumaz; satırları tembel (lazy) biçimde üretir.

    Args:
        yol: Okunacak dosyanın dosya yolu.

    Yields:
        str: Boşlukları temizlenmiş (strip) geçerli satır metni.
    """
    with open(yol, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            temiz = satir.strip()
            if not temiz or temiz.startswith("#"):
                continue
            yield temiz


def ayristir(
    satirlar: Iterable[str],
) -> Generator[tuple[str, str, int], None, None]:
    """'kaynak -> hedef yakit' formatındaki satırlardan (kaynak, hedef, yakit) demeti üretir.

    Args:
        satirlar: Satır metinlerini sağlayan yinelenebilir nesne.

    Yields:
        tuple[str, str, int]: (kaynak, hedef, yakit) demeti.

    Example:
        >>> list(ayristir(["dünya -> sirius 12"]))
        [('dünya', 'sirius', 12)]
    """
    for satir in satirlar:
        if "->" in satir:
            kaynak, hedef_yakit = satir.split("->", 1)
            hedef, yakit_str = hedef_yakit.strip().rsplit(None, 1)
            yield (kaynak.strip(), hedef.strip(), int(yakit_str))


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]],
    esik: int,
) -> Generator[tuple[str, str, int], None, None]:
    """Yakıt miktarı verilen eşikten büyük olan kayıtları süzen üreteç.

    Args:
        kayitlar: (kaynak, hedef, yakit) demetlerini sağlayan yinelenebilir.
        esik: Yakıt süzme eşik değeri.

    Yields:
        tuple[str, str, int]: Yakıt değeri eşikten kesin büyük olan yolculuk kaydı.
    """
    for kayit in kayitlar:
        if kayit[2] > esik:
            yield kayit


def rota_sayaci(baglantilar: dict[str, list[str]]) -> Callable[[str, int], int]:
    """Verilen gezegen bağlantılarına göre rotaları sayan önbellekli fonksiyon üretir.

    İçinde @lru_cache ile süslenmiş rota_sayisi(gezegen, adim) fonksiyonunu tanımlayıp
    döndürür. rota_sayisi, verilen gezegenden başlayıp tam adim yolculuk yapan farklı
    rotaların sayısını hesaplar.

    Args:
        baglantilar: Gezegenler ve gidilebilecek komşuları haritası.

    Returns:
        Callable[[str, int], int]: Önbellekli rota sayma fonksiyonu.
    """
    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Verilen gezegenden başlayarak tam adim yolculuk yapan rota sayısını hesaplar."""
        if adim == 0:
            return 1
        komsular = baglantilar.get(gezegen, [])
        return sum(rota_sayisi(komsu, adim - 1) for komsu in komsular)

    return rota_sayisi


def zamanlayici(aralik: float) -> Generator[bool, None, None]:
    """Belirtilen periyot aralığı dolduğunda True, dolmadığında False üreten meşgul bekleme üreteci.

    Bu üreteç işlemciyi bırakmadan döngüde kontrol gerçekleştirir (meşgul bekleme / busy waiting).
    time.sleep'ten farkı, işletim sistemi çekirdeğine uyku sinyali verip iş parçacığını
    askıya almaması, CPU döngülerini sürekli tüketerek zamanı kontrol etmesidir.

    Args:
        aralik: Tetiklenme aralığı (saniye).

    Yields:
        bool: Aralık tamamlandığında True, aksi halde False.
    """
    son_zaman = time.time()
    while True:
        simdi = time.time()
        if simdi - son_zaman >= aralik:
            son_zaman = simdi
            yield True
        else:
            yield False


def zamanlayici_programi(toplam_sure: float = 10.0, yazdir: bool = True) -> list[tuple[float, str]]:
    """10 saniye boyunca her 2 saniyede 'tik', her 5 saniyede 'tak' yazdıran program.

    Args:
        toplam_sure: Programın toplam çalışma süresi (varsayılan 10 saniye).
        yazdir: Konsola 'tik' ve 'tak' yazdırılıp yazdırılmayacağı.

    Returns:
        list[tuple[float, str]]: Tetiklenen olayların [(zaman, 'tik'/'tak')] listesi.
    """
    t_tik = zamanlayici(2.0)
    t_tak = zamanlayici(5.0)
    baslangic = time.time()
    olaylar: list[tuple[float, str]] = []

    while time.time() - baslangic <= toplam_sure:
        gecen = time.time() - baslangic
        if next(t_tik):
            olaylar.append((gecen, "tik"))
            if yazdir:
                print(f"[{gecen:.2f}s] tik")
        if next(t_tak):
            olaylar.append((gecen, "tak"))
            if yazdir:
                print(f"[{gecen:.2f}s] tak")

    return olaylar
