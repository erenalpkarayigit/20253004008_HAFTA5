# İleri Python Programlama – Hafta 5 Lab Ödevi: Dekoratörler

- **Ders:** İleri Python Programlama  
- **Kurum:** İstanbul Nişantaşı Üniversitesi  
- **Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç  
- **Dönem:** 2026–2027 Güz  
- **Öğrenci:** Eren Alp Karayiğit  
- **Numara:** 20253004008  
- **GitHub Deposu:** [20253004008_HAFTA5](https://github.com/erenalpkarayigit/20253004008_HAFTA5)

---

## Proje Hakkında

Bu proje, Hafta 4 lab çalışmasının devamı olarak geliştirilmiştir. Projeye Python dekoratör mimarisi, `functools.wraps` ile meta veri koruma, dekoratörlerin uygulanma ve icra sırası analizleri, kayıt deseni (registry pattern) ile dinamik komut sistemi, argüman doğrulayan sınır dekoratörleri ve yerleşik kütüphane kullanılmadan closure ile geliştirilmiş bir LRU önbellek (hafıza) dekoratörü eklenmiştir.

Tüm dekoratörler `functools.wraps` kullanır. Eski ve yeni tüm testler `uv run pytest` ile eksiksiz geçmektedir.

---

## Proje Yapısı

```text
20253004008_HAFTA5/
├── README.md
├── dekorator_sirasi.md
├── kapsam.md
├── istatistik.py
├── veri/
│   └── seyir.txt
├── uzay_oyunu/
│   ├── __init__.py
│   ├── akis.py
│   ├── araclar.py
│   ├── dekoratorler.py
│   ├── galaksi.json
│   ├── istatistik.py
│   ├── kayit.py
│   ├── komutlar.py
│   └── oyun.py
└── tests/
    ├── __init__.py
    ├── test_akis.py
    ├── test_dekoratorler.py
    ├── test_fonksiyonlar.py
    └── test_tuzaklar.py
```

---

## Görevler ve Yapılanlar

### Görev 1 – Süre Ölçen Dekoratör (`uzay_oyunu/dekoratorler.py`)
- `sure_olc(fonksiyon)`: Fonksiyonun çalışma süresini `time.perf_counter()` ile ölçüp `“ad: 0.0123 sn”` formatında ekrana yazdırır ve fonksiyonun orijinal dönüş değerini iletir.
- `functools.wraps` kullanılarak `__name__` ve `__doc__` meta verileri korunmuştur.
- Konumsal (`*args`) ve anahtar kelime (`**kwargs`) argümanlarını eksiksiz destekler.
- Hafta 4'teki önbelleksiz rota sayacına uygulanarak performansı doğrulanmıştır.

### Görev 2 – Çağrı Sayacı ve Dekoratör Sırası (`uzay_oyunu/dekoratorler.py` & `dekorator_sirasi.md`)
- `say(fonksiyon)`: Her çağrıda `sarmalayici.cagri` niteliğini 1 artıran çağrı sayacı dekoratörü yazıldı.
- Özyinelemeli `fib(20)` hesaplaması için 3 farklı dekoratör dizilimi test edildi:
  1. **Yalnızca `@say`:** **21.891** çağrı
  2. **`@say` üstte, `@lru_cache` altta:** **39** çağrı
  3. **`@lru_cache` üstte, `@say` altta:** **21** çağrı (erişim: `fib.__wrapped__.cagri`)
- Dekoratörlerin uygulanış sırası ($d_1(d_2(f))$) ve çağrı anındaki yukarıdan aşağıya akış mekanizması [`dekorator_sirasi.md`](dekorator_sirasi.md) belgesinde ayrıntılı olarak açıklanmıştır.

### Görev 3 – Loglayan Dekoratör (`uzay_oyunu/dekoratorler.py` & `oyun.py`)
- `log_cagri(fonksiyon)`: Çağrıdan önce girdi argümanlarını, çağrı sonrasında ise dönüş değerini loglar:
  ```text
  -> yolculuk('orion', hiz=3)
  <- yolculuk = 'orion hiz=3'
  ```
- `galaksi_kur` ve `hedef_menusu` fonksiyonlarına uygulanmış, mevcut testlerin bozulmadan çalıştığı doğrulanmıştır.

### Görev 4 – Komut Sistemi: Kayıt Deseni (`uzay_oyunu/komutlar.py` & `oyun.py`)
- `komut(ad, aciklama="")` dekoratörü ve `KOMUTLAR` sözlüğü geliştirildi.
- Dekoratör fonksiyonu değiştirmeden `(fonksiyon, aciklama)` ikilisi olarak kaydeder. Aynı isimle ikinci kez komut kaydedilmeye çalışıldığında tanım anında `ValueError` fırlatır.
- Oyun durumunu (`durum`) alan üç temel komut tanımlandı:
  - `yardim(durum)`: Kayıtlı tüm komutları ve açıklamalarını alfabetik sırada listeler.
  - `envanter(durum)`: Oyuncunun sahip olduğu eşyaları gösterir.
  - `harita(durum)`: Mevcut konumdan gidilebilecek gezegenleri listeler.
- `travel()` döngüsüne entegre edildi: Oyuncu girdi olarak komut adı girdiğinde komut çalıştırılır, sonuç ekrana basılır ve aynı hedef menüsü yeniden gösterilir.

### Görev 5 – Argüman Alan Sınır Dekoratörü (`uzay_oyunu/dekoratorler.py`)
- `sinirla(alt, ust)`: Dekore edilen fonksiyonun ilk argümanının `[alt, ust]` aralığında olup olmadığını denetler. Aralık dışı durumlarda `ValueError` fırlatır.
- `yakit_harca(miktar)` fonksiyonuna `@sinirla(0, 100)` uygulandı:
  - `yakit_harca(30)` -> `70`
  - `yakit_harca(150)` -> `ValueError: yakit_harca: 150 değeri 0-100 aralığında değil`
- Sınır değerleri (`0`, `100`) ve sınır dışı değerler (`-1`, `101`, `150`) test edildi.

### Bonus (+10 Puan) – Closure Tabanlı Hafıza (LRU Cache) Dekoratörü
- `functools.lru_cache` kullanılmadan, fonksiyon kapanışındaki (closure) sözlük yapısıyla `hafiza(maxsize=None)` dekoratörü geliştirildi.
- `maxsize` parametresi verildiğinde önbellek dolunca en eski kullanılan girdiyi (LRU) tahliye eder.
- Sonuçların `functools.lru_cache` ile birebir aynı değerleri ürettiği test edildi.

---

## Testlerin Çalıştırılması

Tüm test paketini çalıştırmak için:

```bash
uv run pytest -v
```

Test özeti:
```text
tests/test_akis.py .....................                                 [ 36%]
tests/test_dekoratorler.py ....................                          [ 71%]
tests/test_fonksiyonlar.py ..............                                [ 96%]
tests/test_tuzaklar.py ..                                                [100%]

============================= 57 passed in 0.12s ==============================
```
