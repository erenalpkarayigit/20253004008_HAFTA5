"""istatistik.py kök modülü.

PDF yönergesindeki doğrudan `import istatistik` çağrılarını desteklemek amacıyla
tüm fonksiyonları uzay_oyunu.istatistik modülünden içe ve dışa aktarır.
"""

from uzay_oyunu.istatistik import (
    gezegenler_buyuk_harf_map,
    gezegenler_buyuk_harf_comprehension,
    en_az_iki_baglantili_filter,
    en_az_iki_baglantili_comprehension,
    toplam_baglanti_reduce,
    toplam_baglanti_sum,
    yolculuk,
    hizli_yolculuk,
)

__all__ = [
    "gezegenler_buyuk_harf_map",
    "gezegenler_buyuk_harf_comprehension",
    "en_az_iki_baglantili_filter",
    "en_az_iki_baglantili_comprehension",
    "toplam_baglanti_reduce",
    "toplam_baglanti_sum",
    "yolculuk",
    "hizli_yolculuk",
]

if __name__ == "__main__":
    import uzay_oyunu.istatistik
