# Dekoratör Sırası ve Önbellek Etkileşimi Analizi

**Öğrenci:** Eren Alp Karayiğit  
**Numara:** 20253004008  
**Ders:** İleri Python Programlama (Hafta 5 Lab Ödevi)

---

## 1. Giriş ve Dekoratör Çalışma Mantığı

Python'da dekoratörler, fonksiyonların üzerine `@` sembolü ile tanımlandığında **aşağıdan yukarıya** doğru uygulanır:

```python
@dekorator1
@dekorator2
def fonksiyon():
    pass
```

Bu sözdizimi derleme anında şu ifadeye denktir:
$$\text{fonksiyon} = \text{dekorator1}(\text{dekorator2}(\text{fonksiyon}))$$

Ancak bir çağrı yapıldığında icra akışı **yukarıdan aşağıya** (en dıştaki dekoratörden en içtekine) doğru akar. Bu durum, özyinelemeli (recursive) fonksiyonlarda dekoratör sırasının çağrı sayısını ve performansını kökten değiştirmesine neden olur.

---

## 2. Deney Sonuçları (`fib(20)` için)

Özyinelemeli Fibonacci fonksiyonu üç farklı biçimde süslenmiş ve `fib(20)` çağrısı için ölçülen çağrı sayıları aşağıda özetlenmiştir:

| Senaryo | Dekoratör Sırası | Çağrı Sayısı (`cagri`) | Sayaca Erişim Şekli |
| :--- | :--- | :---: | :--- |
| **Senaryo 1** | Yalnızca `@say` | **21891** | `fib1.cagri` |
| **Senaryo 2** | `@say` üstte, `@lru_cache` altta | **39** | `fib2.cagri` |
| **Senaryo 3** | `@lru_cache` üstte, `@say` altta | **21** | `fib3.__wrapped__.cagri` |

---

## 3. Neden Farklı Sonuçlar Ortaya Çıkıyor?

### Senaryo 1: Yalnızca `@say` (21891 Çağrı)
- Fonksiyonda herhangi bir bellek (memoization) mekanizması yoktur.
- $fib(20)$ hesaplanırken aynı alt problemler (örneğin $fib(5)$, $fib(3)$) defalarca yeniden hesaplanır.
- Çağrı sayısı ağacı $C(n) = 1 + C(n-1) + C(n-2)$ bağıntısını takip eder ve $n=20$ için toplam çağrı sayısı tam **21.891** olur.
- `@say` sarmalayıcısı her tekil çağrıyı doğrudan sayar.

### Senaryo 2: `@say` Üstte, `@lru_cache` Altta (39 Çağrı)
- Yapı: `say(lru_cache(fib))`
- Fonksiyon çağrıldığında en dış katman `@say` dekoratörüdür.
- `fib(n-1)` veya `fib(n-2)` özyinelemeli olarak çağrıldığında, isim alanındaki `fib` değişkeni en dıştaki `@say` fonksiyonuna işaret ettiği için her çağrıda önce `@say` sayacı bir artırılır, ardından alttaki `@lru_cache` katmanına geçilir.
- `@lru_cache` altta olduğu için önbellekteki değer hemen döndürülse bile, çağrı isteği en dıştaki `@say` süzgecinden geçmiş olur.
- $fib(20)$'den $fib(0)$'a kadar hesaplama ağacında toplam 39 kez fonksiyon giriş kapısından geçilir ($2 \times 20 - 1 = 39$).

### Senaryo 3: `@lru_cache` Üstte, `@say` Altta (21 Çağrı)
- Yapı: `lru_cache(say(fib))`
- En dış katmanda `@lru_cache` yer almaktadır.
- Fonksiyon çağrıldığında istek ilk olarak `@lru_cache` tarafından karşılanır.
- Eğer çağrılan argüman (örneğin $fib(5)$) daha önce hesaplanmış ve önbelleğe alınmışsa (cache hit), `@lru_cache` sonucu **alttaki `@say` fonksiyonunu hiç çalıştırmadan** anında döndürür.
- `@say` dekoratörü yalnızca bir önbellek ıskalaması (cache miss) meydana geldiğinde, yani değer ilk defa hesaplanırken tetiklenir.
- $0 \le n \le 20$ aralığında toplam 21 benzersiz sayı ($0, 1, 2, \dots, 20$) olduğu için `@say` yalnızca 21 kez çalışır.

#### `fib.__wrapped__.cagri` İpucunun Açıklaması:
Senaryo 3'te dıştaki nesne `@lru_cache` sarmalayıcısıdır. `@say` dekoratörünün tanımladığı `cagri` niteliği içteki fonksiyona aittir. `functools.wraps` sayesinde içteki fonksiyona `__wrapped__` zinciri üzerinden erişilebilir: bu nedenle sayaca doğrudan `fib.cagri` yerine `fib.__wrapped__.cagri` şeklinde ulaşılır.
