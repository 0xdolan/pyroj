# Locale Reference

This is the complete locale and dialect reference for `pyroj`.

## Canonical Locales

| Code | Enum | Notes |
| --- | --- | --- |
| `ckb` | `LocaleId.CKB` | Sorani canonical locale |
| `kmr` | `LocaleId.KMR` | Kurmanji canonical locale |
| `ku` | `LocaleId.KU` | Compatibility alias (`ku -> ckb`) |
| `en` | `LocaleId.EN` | English |
| `fa` | `LocaleId.FA` | Persian |
| `ar` | `LocaleId.AR` | Arabic |
| `tr` | `LocaleId.TR` | Turkish |

## Alias Resolution

| Input code | Resolves to | Runtime intent |
| --- | --- | --- |
| `sdh` | `ckb` | Kalhori/Southern Kurdish family |
| `lki` | `ckb` | Laki family |
| `hac` | `ckb` | Hawrami/Gorani family |
| `zza` | `kmr` | Zazaki macrolanguage |
| `diq` | `kmr` | Southern Zazaki |
| `kiu` | `kmr` | Northern Zazaki |
| `ku-latn`, `ku_latn` | `kmr` | Kurdish Latin script alias |
| `ku` | `ckb` | Backward-compatible Kurdish alias |

## Kurdish Variant Keys

Pass these keys to `kurdish_variant=` when formatting Kurdish calendar names:

- `standard`
- `sdh_kelhuri`
- `lki_laki`
- `hac_hawrami`
- `zza_zazaki`
- `syriac`

## Month Tables (Source-Aligned)

Baseline for regional forms is the unified Kurdish month table. Note that some months have multiple valid names. When formatting, `pyroj` defaults to the first name listed, but developers can access alternatives natively via `get_locale(LocaleId.CKB).names(CalendarKind.KURDISH).months`.

### 'standard'

| # | CKB Names | KMR Names |
| --- | --- | --- |
| 1 | خاکه‌لێوه, نەورۆز, ھەرمێ پشکوان | Nîsan, Newroz, Herme Pişkewan |
| 2 | گوڵان | Gulan |
| 3 | جۆزه‌ردان | Hezîran |
| 4 | پوشپه‌ر | Tîrmeh |
| 5 | گه‌لاوێژ | Gelawêj |
| 6 | خه‌رمانان | Îlon |
| 7 | ره‌زبه‌ر | Rezber |
| 8 | گه‌ڵارێزان | Gellarêzan |
| 9 | سه‌رماوه‌ز | Sermawez |
| 10 | به‌فرانبار | Befranbar |
| 11 | رێبه‌ندان | Rêbendan |
| 12 | ره‌شه‌مێ | Reşemê |

### 'sdh_kelhuri'

| # | CKB Names | KMR Names |
| --- | --- | --- |
| 1 | جەژنان | Cejnan |
| 2 | گوڵان | Gulan |
| 3 | زەردان | Zerdan |
| 4 | پەرپەر | Perper |
| 5 | گه‌لاویژ | Gelawêj |
| 6 | نوخشان | Noxşan |
| 7 | بەران | Beran |
| 8 | خەزان | Xezan |
| 9 | ساران | Saran |
| 10 | بەفران | Befran |
| 11 | بەندان | Bendan |
| 12 | رەمشان | Remşan |

### 'lki_laki'

| # | CKB Names | KMR Names |
| --- | --- | --- |
| 1 | پەنجە | Pence |
| 2 | میریان | Miryan |
| 3 | گاکووڕ | Gakûr |
| 4 | ئاگرانی | Agranî |
| 5 | مردار | Mirdar |
| 6 | ماڵەژێر | Malajêr |
| 7 | ماڵەژێر دوماینە | Malajêr 2 |
| 8 | تۊلتەکن | Tultek |
| 9 | مانگ سیە | Mang Sî |
| 10 | نۆڕووژ | Norûj |
| 11 | خاکەلیە | Xakelî |
| 12 | مانگ لیە | Mang Lî |

### 'hac_hawrami'

| # | CKB Names | KMR Names |
| --- | --- | --- |
| 1 | نەوڕۆز | Newroz |
| 2 | پاژەرەژ | Pajerej |
| 3 | چێڵکڕ | Çêlkr |
| 4 | کۆپڕ | Kopr |
| 5 | گه‌لاوێژ | Gelawêj |
| 6 | ئاوەوەرە | Awewere |
| 7 | ترازیێ | Terazî |
| 8 | گه‌ڵاخەزان | Gelaxezan |
| 9 | کەڵەھەرز | Keleherz |
| 10 | ئارگا | Arga |
| 11 | رابڕان | Rabran |
| 12 | سیاوکام | Siyawkam |

### 'zza_zazaki'

| # | CKB Names | KMR Names |
| --- | --- | --- |
| 1 | نیسانە | Nîsan |
| 2 | گولانە | Gulan |
| 3 | ھەزیرانە, ڤارتڤارە, ئامنانو ڤەرێن, ئامنانیا ڤەرێنە | Hezîran, Vartvar, Amano Verên, Amaniya Verêne |
| 4 | تەممووزە | Temmuz |
| 5 | تەباخە, ئامنانو پەیێن, ئامنانیا پەیێنە, ئاگوستە | Tebax, Amano Peyên, Amaniya Peyêne, Awuste |
| 6 | کەشکەلون, جتمەنگی, ئێلولە, ئەلون, ئیلۆنە, پاییزو ڤەرێن, پاییزیا ڤەرێنە | Keshkelon, Ctemengi, Îlule, Elon, Îlonê, Payîzo Verên, Payîzya Verêne |
| 7 | تشرینو ڤەرێن, پاییزە, پاییزو وەرتێن, پاییزیا وەرتێنە | Tişrino Verên, Payîza, Payîzo Werten, Payîzya Wertenê |
| 8 | تشرینو پەیێن, بارانڤەردانە, گاڤارە, کەلڤەردانە, ناخلقرانە, پاییزو پەیێن, پاییزیا پەیێنە | Tişrino Peyên, Baranverdene, Gavare, Kelverde, Naxelqerane, Payîzo Peyên, Payîzya Peyêne |
| 9 | تشرینو پەیێن, بارانڤەردانە, گاڤارە, کەلڤەردانە, ناخلقرانە, پاییزو پەیێن, پاییزیا پەیێنە | Tişrino Peyên, Baranverdene, Gavare, Kelverde, Naxelqerane, Payîzo Peyên, Payîzya Peyêne |
| 10 | چلە, چلە, چەلییە, چەلەیو پل, چلەی وەرتی, زەمپەریە, زقناوتە, زقناووتە | Çile, Çile, Çêliye, Çileyo Pel, Çiley Werti, Zemperî, Zqnewte, Zqnewte |
| 11 | سباتە, گوجگە, گوژگە, چەڵەیو پەیێن, چلەیو پەیێن | Sibat, Gujge, Gujge, Çileyo Peyên, Çileyo Peyên |
| 12 | ئادار, ئادارە, ئاودار, مارتە | Adar, Adare, Audar, Marte |

### 'syriac'

| # | CKB Names | KMR Names |
| --- | --- | --- |
| 1 | کانوونی دووه‌م | Kanûnê Duyem |
| 2 | شوبات | Şubat |
| 3 | ئازار | Adar |
| 4 | نیسان | Nîsan |
| 5 | ئایار | Gulan |
| 6 | حوزەیران | Hezîran |
| 7 | تەممووز | Tîrmeh |
| 8 | ئاب | Tebax |
| 9 | کانون | Kanûn |
| 10 | تشرینی یەکەم | Tişrîn 1 |
| 11 | تشرینی دووه‌م | Tişrîn 2 |
| 12 | کانوونی یەکەم | Kanûnê Yekem |

## Usage Examples

```python
from datetime import date
from pyroj import CalendarKind, KurdishDate, format_calendar_date

kd = KurdishDate.from_gregorian(date(2026, 3, 24))

# Canonical defaults
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="ckb"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="kmr"))

# Variant selection
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="kmr", kurdish_variant="syriac"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="sdh", kurdish_variant="sdh_kelhuri"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="lki", kurdish_variant="lki_laki"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="hac", kurdish_variant="hac_hawrami"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="zza", kurdish_variant="zza_zazaki"))
```
