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
- `gelarêzan` (or `gelarezan`)
- `kmr_wikipedia`
- `sdh_kelhuri`
- `lki_laki`
- `hac_hawrami`
- `zza_zazaki`

## Month Tables (Source-Aligned)

Baseline for regional forms is the Kurdish month table from CKB Wikipedia:
[مانگە کوردییەکان - ویکیپیدیا](https://ckb.wikipedia.org/wiki/%D9%85%D8%A7%D9%86%DA%AF%DB%95_%DA%A9%D9%88%D8%B1%D8%AF%DB%8C%DB%8C%DB%95%DA%A9%D8%A7%D9%86)

### `ckb` Sorani

| # | `standard` | `gelarêzan` |
| --- | --- | --- |
| 1 | خاکەلێوە | خاکەلێوە |
| 2 | گوڵان | گوڵان |
| 3 | جۆزەردان | جۆزەردان |
| 4 | پووشپەڕ | پووشپەڕ |
| 5 | گەلاوێژ | گەلاوێژ |
| 6 | خەرمانان | خەرمانان |
| 7 | ڕەزبەر | ڕەزبەر |
| 8 | خەزەڵوەر | گەڵاڕێزان |
| 9 | سەرماوەز | سەرماوەز |
| 10 | بەفرانبار | بەفرانبار |
| 11 | ڕێبەندان | ڕێبەندان |
| 12 | ڕەشەمە | ڕەشەمێ |

### `kmr` Kurmanji

| # | `standard` | `gelarêzan` | `kmr_wikipedia` |
| --- | --- | --- | --- |
| 1 | Xakelêwe | Xakelêwe | Nîsan |
| 2 | Gulan | Gulan | Gulan |
| 3 | Cozerdan | Cozerdan | Hezîran |
| 4 | Pûşper | Pûşper | Tîrmeh |
| 5 | Gelawêj | Gelawêj | Îlon |
| 6 | Xermanan | Xermanan | Tebax |
| 7 | Rezber | Rezber | Cotmeh |
| 8 | Xezelwer | Gelarêzan | Mijdar |
| 9 | Sermawez | Sermawez | Kanûn |
| 10 | Befranbar | Befranbar | Çile |
| 11 | Rêbendan | Rêbendan | Sibat |
| 12 | Reşemê | Reşemê | Adar |

### `sdh` Kalhori (`sdh_kelhuri`)

| # | Month |
| --- | --- |
| 1 | جەشنان |
| 2 | گوڵان |
| 3 | زەردان |
| 4 | پەرپەر |
| 5 | نوخشان |
| 6 | گەلاوێژ |
| 7 | بەران |
| 8 | خەزان |
| 9 | ساران |
| 10 | بەفران |
| 11 | بەندان |
| 12 | رەمشان |

### `lki` Laki (`lki_laki`)

| # | Month |
| --- | --- |
| 1 | پەنجە |
| 2 | میریان |
| 3 | گاکووڕ |
| 4 | ئاگرانی |
| 5 | ماڵەژێر |
| 6 | مردار |
| 7 | ماڵەژێر دوماینە |
| 8 | تۊلتەکن |
| 9 | مانگ سیە |
| 10 | نۆڕووژ |
| 11 | خاکەلیە |
| 12 | مانگ لیە |

### `hac` Hawrami (`hac_hawrami`)

| # | Month |
| --- | --- |
| 1 | نەوڕۆز |
| 2 | پاژەرەژ |
| 3 | چێڵکڕ |
| 4 | کۆپڕ |
| 5 | ئاوەوەرە |
| 6 | گەلاوێژ |
| 7 | ترازیێ |
| 8 | گەڵاخەزان |
| 9 | کەڵەھەرز |
| 10 | ئارگا |
| 11 | رابڕان |
| 12 | سیاوکام |

### `zza` Zazaki (`zza_zazaki`)

| # | Month |
| --- | --- |
| 1 | نیسانە/لیزان |
| 2 | گولانە |
| 3 | ھەزیرانە/ڤارتڤارە/ئامنانو ڤەرێن/ئامنانیا ڤەرێنە |
| 4 | تەممووزە/مەنگا پالی/تەخترما/تیرمەنگ |
| 5 | کەشکەلون/جتمەنگی/ئێلولە/ئەلون/ئیلۆنە/پاییزو ڤەرێن/پاییزیا ڤەرێنە |
| 6 | تەباخە/ئامنانو پەیێن/ئامنانیا پەیێنە/ئاگوستە |
| 7 | تشرینو ڤەرێن/پاییزە/پاییزو وەرتێن/پاییزیا وەرتێنە |
| 8 | تشرینو پەیێن/بارانڤەردانە/گاڤارە/کەلڤەردانە/ناخلقرانە/پاییزو پەیێن/پاییزیا پەیێنە |
| 9 | کانون/گاغان/تاڤارە/چلەیو ڤەرێن/چلەیو قج |
| 10 | چەلە/چلە/چەلییە/چەلەیو پل/چلەی وەرتی/زەمپەریە/زقناوتە/زقناووتە |
| 11 | سباتە/گوجگە/گوژگە/چەلەیو پەیێن/چلەیو پەیێن |
| 12 | ئادار/ئادارە/ئاودار/مارتە |

## Usage Examples

```python
from datetime import date
from pyroj import CalendarKind, KurdishDate, format_calendar_date

kd = KurdishDate.from_gregorian(date(2026, 3, 24))

# Canonical defaults
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="ckb"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="kmr"))

# Variant selection
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="kmr", kurdish_variant="kmr_wikipedia"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="sdh", kurdish_variant="sdh_kelhuri"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="lki", kurdish_variant="lki_laki"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="hac", kurdish_variant="hac_hawrami"))
print(format_calendar_date(kd, "%B", calendar=CalendarKind.KURDISH, locale="zza", kurdish_variant="zza_zazaki"))
```
