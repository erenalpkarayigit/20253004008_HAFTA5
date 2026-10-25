# İleri Python Programlama – Hafta 4 Lab Ödevi: Üreteçler ve functools

- **Ders:** İleri Python Programlama  
- **Kurum:** İstanbul Nişantaşı Üniversitesi  
- **Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç  
- **Dönem:** 2026–2027 Güz  
- **Öğrenci:** Eren Alp Karayiğit  
- **Numara:** 20253004008  
- **GitHub Deposu:** [20253004008_HAFTA4](https://github.com/erenalpkarayigit/20253004008_HAFTA4)

---

## Proje Hakkında

Bu proje, Hafta 3'teki uzay oyunu projesinin üzerine inşa edilmiştir. Projeye üreteçler (generators), tembel değerlendirmeli (lazy evaluation) bir veri boru hattı, `@functools.lru_cache` ile optimize edilmiş bir rota hesaplama sayacı, fonksiyonel programlama araçları (`map`, `filter`, `reduce`, `partial`) ve meşgul bekleme (busy waiting) zamanlayıcısı eklenmiştir.

Tüm fonksiyonlarda tam tip ipuçları (type hints) ve docstring'ler eksiksiz yer almakta; eski ve yeni tüm testler `uv run pytest` ile başarıyla geçmektedir.

---

## Proje Yapısı

```text
20253004008_HAFTA4/
├── README.md
├── kapsam.md
├── istatistik.py
├── veri/
│   └── seyir.txt
├── uzay_oyunu/
│   ├── __init__.py
│   ├── akis.py
│   ├── istatistik.py
│   ├── oyun.py
│   ├── kayit.py
│   ├── araclar.py
│   └── galaksi.json
└── tests/
    ├── __init__.py
    ├── test_akis.py
    ├── test_fonksiyonlar.py
    └── test_tuzaklar.py
```

---

## Görevler ve Yapılanlar

### Görev 1 – Fibonacci Üreteci (`uzay_oyunu/akis.py`)
- `fibonacci() -> Generator[int, None, None]`: Sonsuz Fibonacci dizisi üreten saf bir üreteçtir.
- Değerler üç farklı yolla alınmıştır:
  1. `next()` ile ilk 3 değer: `(0, 1, 1)`
  2. `itertools.islice()` ile ilk 12 değer: `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]`
  3. `itertools.takewhile()` ile 100'den küçük değerler: `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]`
- **Tek Kullanımlık Testi:** Üretecin tek kullanımlık olduğu gösterilmiş; aynı üreteç nesnesinden arka arkaya yapılan iki `list(islice(g, 5))` çağrısının `[0, 1, 1, 2, 3]` ve `[5, 8, 13, 21, 34]` şeklinde farklı sonuçlar ürettiği `tests/test_akis.py` içinde doğrulanmıştır.

### Görev 2 – Yakıt Göstergesi (`uzay_oyunu/akis.py` & `oyun.py`)
- `yakit_gostergesi(yakit: int, tuketim: int) -> Generator[int, None, None]`: Her `next()` çağrısında yakıtı `tuketim` kadar azaltıp kalan yakıtı üretir, yakıt sıfıra inince durur (`StopIteration` fırlatır).
  - Örnek: `list(yakit_gostergesi(100, 30))` -> `[70, 40, 10, 0]`
- `travel()` fonksiyonu içerisine oyun başında galaksideki yakıt miktarıyla gösterge entegre edilmiştir. Her yolculukta göstergeden yeni bir değer çekilir; `StopIteration` yakalandığında `"Yakıtın bitti, uzayda sürükleniyorsun…"` mesajıyla oyun mağlubiyetle sonlandırılır.

### Görev 3 – Seyir Defteri Boru Hattı (`veri/seyir.txt` & `uzay_oyunu/akis.py`)
- `veri/seyir.txt` veri dosyası oluşturulmuştur.
- Üç üreteçten oluşan tembel (lazy) veri işleme boru hattı kurulmuştur:
  1. `satirlari_oku(yol)`: Boş satırları ve `#` ile başlayan yorum satırlarını atlar.
  2. `ayristir(satirlar)`: Her satırdan `(kaynak, hedef, yakit)` demeti üretir.
  3. `uzun_yolculuklar(kayitlar, esik)`: Yakıtı eşik değerinden büyük olan kayıtları süzer.
- Hiçbir aşama dosyayı tümüyle bir listeye okumaz; tüm boru hattı bellek dostu üreteçler üzerinde akar.
  - `sum(y for _, _, y in ayristir(satirlari_oku("veri/seyir.txt")))` -> `88`
  - `[h for _, h, _ in uzun_yolculuklar(kayitlar, 10)]` -> `['sirius', 'centauri', 'orion', 'kara_delik']`

### Görev 4 – Önbellekli Rota Sayacı (`uzay_oyunu/akis.py`)
- `rota_sayaci(baglantilar)`: İçinde `@functools.lru_cache(maxsize=None)` ile süslenmiş özyinelemeli `rota_sayisi(gezegen, adim)` fonksiyonunu tanımlayıp döndürür. Verilen gezegenden başlayıp tam `adim` yolculuk yapan rota sayısını hesaplar.
  - `say("dünya", 3)` -> `9`
  - `say("dünya", 10)` -> `2185`
  - `say("dünya", 40)` -> `16832258606399`

#### Ölçümler ve Karşılaştırma (`adim = 20` için):

| Metrik | Önbelleksiz Sürüm | Önbellekli Sürüm (`@lru_cache`) |
| :--- | :--- | :--- |
| **Sonuç (Rota Sayısı)** | 4.315.343 | 4.315.343 |
| **Çalışma Süresi** | ~0.728464 saniye | ~0.000064 saniye |
| **Hızlanma Çarpanı** | 1x (Referans) | **~11.435 kat daha hızlı** |
| **`cache_info()` Çıktısı** | Yok | `CacheInfo(hits=47, misses=51, maxsize=None, currsize=51)` |

Önbellekleme sayesinde üstel karmaşıklık ($O(b^d)$) doğrusal karmaşıklığa ($O(N \cdot d)$) indirilmiş ve rota hesaplamaları anlık seviyeye çekilmiştir.

### Görev 5 – map, filter, reduce ve partial (`uzay_oyunu/istatistik.py` & `istatistik.py`)
Galaksi verisi üzerinde aynı 3 soru iki farklı yöntemle (önce `map`/`filter`/`reduce`, sonra liste üreteci veya `sum`) yanıtlanmıştır:
1. **Gezegen adlarının büyük harfli listesi:**
   - `gezegenler_buyuk_harf_map()` & `gezegenler_buyuk_harf_comprehension()`
   - Çıktı: `['DÜNYA', 'CENTAURI', 'SIRIUS', 'ORION', 'KARA_DELIK']`
2. **En az iki bağlantısı olan gezegenler:**
   - `en_az_iki_baglantili_filter()` & `en_az_iki_baglantili_comprehension()`
   - Çıktı: `['dünya', 'centauri', 'sirius', 'orion']`
3. **Toplam bağlantı sayısı:**
   - `toplam_baglanti_reduce()` & `toplam_baglanti_sum()`
   - Çıktı: `10`
4. **`functools.partial` Kullanımı:**
   - `yolculuk(mesafe, hiz=1.0)` fonksiyonundan `hiz=3.0` sabitlenerek `hizli_yolculuk` türetilmiştir.

#### Okunabilirlik Değerlendirmesi:
> Python'da liste üreteçleri (list comprehensions) ve `sum()`, `map()` / `filter()` / `reduce()` kombinasyonlarına göre çok daha "Pythonic", doğrudan ve okunaklıdır. Lambda ifadelerinin getirdiği sözdizimi yükünü ve fazladan `list()` dönüşüm ihtiyacını ortadan kaldırır. `functools.partial` ise bir fonksiyonun parametrelerini sabitleyip yeni bir fonksiyonel varyant üretmek için son derece temiz ve deklaratiftir.

### Bonus (+10 Puan) – Zamanlayıcı ve Meşgul Bekleme (`uzay_oyunu/akis.py`)
- `zamanlayici(aralik)` üreteci kullanılarak 10 saniye boyunca her 2 saniyede "tik", her 5 saniyede "tak" üreten program geliştirilmiştir.
- **Meşgul Bekleme (Busy Waiting) ve `time.sleep` Farkı:**
  - **Meşgul Bekleme (Busy Waiting):** İş parçacığı CPU'yu bırakmaz; zaman şartı sağlanana kadar bir döngü içinde sürekli saat kontrolü yapar (`while True: if time.time() - son >= aralik`). Bu süreçte CPU çekirdeği %100 kullanımda tutulur ve işlemci boş yere enerji harcar.
  - **`time.sleep()`:** İş parçacığını işletim sistemi çekirdeği düzeyinde askıya alır (blocked/sleeping durumuna geçirir). İşletim sistemi zamanlayıcısı CPU'yu diğer işlemlere tahsis eder; süre dolduğunda donanım zamanlayıcı kesmesiyle (timer interrupt) iş parçacığı uyandırılır. Bu esnada CPU kullanımı %0'dır.

---

## Testlerin Çalıştırılması

Tüm eski (Hafta 3) ve yeni (Hafta 4) testler `uv run pytest` komutu ile çalıştırılabilir:

```bash
uv run pytest -v
```

Çıktı özeti:
```text
tests/test_akis.py ..................... [ 56%]
tests/test_fonksiyonlar.py .............. [ 94%]
tests/test_tuzaklar.py ..                [100%]

============================= 37 passed in 0.12s ==============================
```
