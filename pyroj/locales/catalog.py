"""Load locale month/weekday tables from ``catalog.json`` (package data)."""

from __future__ import annotations

import json
from importlib import resources
from typing import cast

from pyroj.locales.types import CalendarNames, LocaleData, LocaleId

_LOCALE_ALIASES: dict[str, LocaleId] = {
    "en": LocaleId.EN,
    "ku": LocaleId.KU,
    "kmr": LocaleId.KMR,
    "ckb": LocaleId.CKB,
    "fa": LocaleId.FA,
    "tr": LocaleId.TR,
    "ar": LocaleId.AR,
    # Additional Kurdish-related ISO 639-3 codes.
    "sdh": LocaleId.CKB,  # Southern Kurdish / Kalhori (Arabic script family)
    "lki": LocaleId.CKB,  # Laki (Arabic script family)
    "hac": LocaleId.CKB,  # Hawrami/Gorani (often Arabic script in this ecosystem)
    "zza": LocaleId.KMR,  # Zazaki macrolanguage (commonly Latin-script deployments)
    "diq": LocaleId.KMR,  # Southern Zazaki
    "kiu": LocaleId.KMR,  # Northern Zazaki
    # Script aliases
    "ku-latn": LocaleId.KMR,
    "ku_latn": LocaleId.KMR,
}

# Keep KU as a compatibility alias that resolves to Sorani/Arabic tables by default.
_COMPAT_LOCALE_REDIRECTS: dict[LocaleId, LocaleId] = {
    LocaleId.KU: LocaleId.CKB,
}


def _calendar_names(obj: object) -> CalendarNames:
    d = obj if isinstance(obj, dict) else {}
    return CalendarNames(
        months=tuple(d["months"]),
        months_short=tuple(d["months_short"]),
        weekdays=tuple(d["weekdays"]),
        weekdays_short=tuple(d["weekdays_short"]),
        weekdays_min=tuple(d["weekdays_min"]),
    )


def _load_raw() -> dict[str, object]:
    text = resources.files("pyroj.locales").joinpath("catalog.json").read_text(encoding="utf-8")
    data: object = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("catalog.json must contain a JSON object at the root")
    return cast(dict[str, object], data)


def _build_locale_by_id() -> dict[LocaleId, LocaleData]:
    raw = _load_raw()
    locales = raw["locales"]
    if not isinstance(locales, dict):
        raise ValueError("catalog.json: invalid 'locales'")
    out: dict[LocaleId, LocaleData] = {}
    for key, block in locales.items():
        if not isinstance(block, dict):
            continue
        lid = LocaleId[str(key).upper()]
        out[lid] = LocaleData(
            locale_id=lid,
            gregorian=_calendar_names(block["gregorian"]),
            persian=_calendar_names(block["persian"]),
            kurdish=_calendar_names(block["kurdish"]),
            islamic=_calendar_names(block["islamic"]),
            digits=tuple(block["digits"]),
            am_pm=(block["am_pm"][0], block["am_pm"][1]),
        )
    return out


LOCALE_BY_ID: dict[LocaleId, LocaleData] = _build_locale_by_id()


def get_locale(locale_id: LocaleId) -> LocaleData:
    """Return :class:`LocaleData` for ``locale_id``."""
    return LOCALE_BY_ID[resolve_locale(locale_id)]


def resolve_locale(locale: LocaleId | str, *, default: LocaleId = LocaleId.EN) -> LocaleId:
    """Resolve enum/string locale input to a known ``LocaleId`` with deterministic fallback."""
    lid = _resolve_locale_input(locale)
    if lid is None:
        return default
    normalized = _COMPAT_LOCALE_REDIRECTS.get(lid, lid)
    if normalized in LOCALE_BY_ID:
        return normalized
    return default


def get_locale_resolved(locale: LocaleId | str, *, default: LocaleId = LocaleId.EN) -> LocaleData:
    """Resolve ``locale`` then return its locale data."""
    return LOCALE_BY_ID[resolve_locale(locale, default=default)]


def get_kurdish_month_variant(
    locale: LocaleId | str,
    variant: str | None,
    *,
    default: LocaleId = LocaleId.EN,
) -> CalendarNames | None:
    """
    Return Kurdish month-name variant data for a locale.

    ``None`` means "use locale default names". Unknown variants return ``None``.
    """
    if not variant:
        return None
    lid = resolve_locale(locale, default=default)
    key = variant.strip().lower().replace(" ", "_").replace("-", "_")
    return _KURDISH_MONTH_VARIANTS.get(lid, {}).get(key)


def _resolve_locale_input(locale: LocaleId | str) -> LocaleId | None:
    if isinstance(locale, LocaleId):
        return locale
    key = locale.strip().lower()
    if not key:
        return None
    direct = _LOCALE_ALIASES.get(key)
    if direct is not None:
        return direct
    enum_key = key.replace("-", "_").upper()
    if enum_key in LocaleId.__members__:
        return LocaleId[enum_key]
    return None


_KURDISH_MONTH_VARIANTS: dict[LocaleId, dict[str, CalendarNames]] = {
    LocaleId.CKB: {
        "standard": CalendarNames(
            months=(
                "خاکەلێوە",
                "گوڵان",
                "جۆزەردان",
                "پووشپەڕ",
                "گەلاوێژ",
                "خەرمانان",
                "ڕەزبەر",
                "خەزەڵوەر",
                "سەرماوەز",
                "بەفرانبار",
                "ڕێبەندان",
                "ڕەشەمە",
            ),
            months_short=(
                "خاک",
                "گوڵان",
                "جۆزەرد",
                "پووشپەڕ",
                "گەلاوێژ",
                "خەرمان",
                "ڕەزبەر",
                "خەزەڵ",
                "سەرما",
                "بەفران",
                "ڕێبەند",
                "ڕەشەمە",
            ),
            weekdays=(
                "شەممە",
                "یەکشەممە",
                "دووشەممە",
                "سێشەممە",
                "چوارشەممە",
                "پێنجشەممە",
                "هەینی",
            ),
            weekdays_short=("شەممە", "یەک", "دوو", "سێ", "چوار", "پێنج", "هەینی"),
            weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "ه"),
        ),
        "gelarêzan": CalendarNames(
            months=(
                "خاکەلێوە",
                "گوڵان",
                "جۆزەردان",
                "پووشپەڕ",
                "گەلاوێژ",
                "خەرمانان",
                "ڕەزبەر",
                "گەڵاڕێزان",
                "سەرماوەز",
                "بەفرانبار",
                "ڕێبەندان",
                "ڕەشەمێ",
            ),
            months_short=(
                "خاک",
                "گوڵان",
                "جۆزەرد",
                "پووشپەڕ",
                "گەلاوێژ",
                "خەرمان",
                "ڕەزبەر",
                "گەڵاڕێز",
                "سەرما",
                "بەفران",
                "ڕێبەند",
                "ڕەشەمێ",
            ),
            weekdays=(
                "شەممە",
                "یەکشەممە",
                "دووشەممە",
                "سێشەممە",
                "چوارشەممە",
                "پێنجشەممە",
                "هەینی",
            ),
            weekdays_short=("شەممە", "یەک", "دوو", "سێ", "چوار", "پێنج", "هەینی"),
            weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "ه"),
        ),
        "gelarezan": CalendarNames(
            months=(
                "خاکەلێوە",
                "گوڵان",
                "جۆزەردان",
                "پووشپەڕ",
                "گەلاوێژ",
                "خەرمانان",
                "ڕەزبەر",
                "گەڵاڕێزان",
                "سەرماوەز",
                "بەفرانبار",
                "ڕێبەندان",
                "ڕەشەمێ",
            ),
            months_short=(
                "خاک",
                "گوڵان",
                "جۆزەرد",
                "پووشپەڕ",
                "گەلاوێژ",
                "خەرمان",
                "ڕەزبەر",
                "گەڵاڕێز",
                "سەرما",
                "بەفران",
                "ڕێبەند",
                "ڕەشەمێ",
            ),
            weekdays=(
                "شەممە",
                "یەکشەممە",
                "دووشەممە",
                "سێشەممە",
                "چوارشەممە",
                "پێنجشەممە",
                "هەینی",
            ),
            weekdays_short=("شەممە", "یەک", "دوو", "سێ", "چوار", "پێنج", "هەینی"),
            weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "ه"),
        ),
        "sdh_kelhuri": CalendarNames(
            months=(
                "جەشنان",
                "گوڵان",
                "زەردان",
                "پەرپەر",
                "نوخشان",
                "گەلاوێژ",
                "بەران",
                "خەزان",
                "ساران",
                "بەفران",
                "بەندان",
                "رەمشان",
            ),
            months_short=(
                "جەشنان",
                "گوڵان",
                "زەردان",
                "پەرپەر",
                "نوخشان",
                "گەلاوێژ",
                "بەران",
                "خەزان",
                "ساران",
                "بەفران",
                "بەندان",
                "رەمشان",
            ),
            weekdays=(
                "شەممە",
                "یەکشەممە",
                "دووشەممە",
                "سێشەممە",
                "چوارشەممە",
                "پێنجشەممە",
                "هەینی",
            ),
            weekdays_short=("شەممە", "یەک", "دوو", "سێ", "چوار", "پێنج", "هەینی"),
            weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "ه"),
        ),
        "lki_laki": CalendarNames(
            months=(
                "پەنجە",
                "میریان",
                "گاکووڕ",
                "ئاگرانی",
                "ماڵەژێر",
                "مردار",
                "ماڵەژێر دوماینە",
                "تۊلتەکن",
                "مانگ سیە",
                "نۆڕووژ",
                "خاکەلیە",
                "مانگ لیە",
            ),
            months_short=(
                "پەنجە",
                "میریان",
                "گاکووڕ",
                "ئاگرانی",
                "ماڵەژێر",
                "مردار",
                "ماڵەژێر2",
                "تۊلتەکن",
                "مانگ سیە",
                "نۆڕووژ",
                "خاکەلیە",
                "مانگ لیە",
            ),
            weekdays=(
                "شەممە",
                "یەکشەممە",
                "دووشەممە",
                "سێشەممە",
                "چوارشەممە",
                "پێنجشەممە",
                "هەینی",
            ),
            weekdays_short=("شەممە", "یەک", "دوو", "سێ", "چوار", "پێنج", "هەینی"),
            weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "ه"),
        ),
        "hac_hawrami": CalendarNames(
            months=(
                "نەوڕۆز",
                "پاژەرەژ",
                "چێڵکڕ",
                "کۆپڕ",
                "ئاوەوەرە",
                "گەلاوێژ",
                "ترازیێ",
                "گەڵاخەزان",
                "کەڵەھەرز",
                "ئارگا",
                "رابڕان",
                "سیاوکام",
            ),
            months_short=(
                "نەوڕۆز",
                "پاژەر",
                "چێڵکڕ",
                "کۆپڕ",
                "ئاوەوەر",
                "گەلاوێژ",
                "ترازیێ",
                "گەڵاخەز",
                "کەڵەھەرز",
                "ئارگا",
                "رابڕان",
                "سیاوکام",
            ),
            weekdays=(
                "شەممە",
                "یەکشەممە",
                "دووشەممە",
                "سێشەممە",
                "چوارشەممە",
                "پێنجشەممە",
                "هەینی",
            ),
            weekdays_short=("شەممە", "یەک", "دوو", "سێ", "چوار", "پێنج", "هەینی"),
            weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "ه"),
        ),
        "zza_zazaki": CalendarNames(
            months=(
                "نیسانە/لیزان",
                "گولانە",
                "ھەزیرانە/ڤارتڤارە/ئامنانو ڤەرێن/ئامنانیا ڤەرێنە",
                "تەممووزە/مەنگا پالی/تەخترما/تیرمەنگ",
                "کەشکەلون/جتمەنگی/ئێلولە/ئەلون/ئیلۆنە/پاییزو ڤەرێن/پاییزیا ڤەرێنە",
                "تەباخە/ئامنانو پەیێن/ئامنانیا پەیێنە/ئاگوستە",
                "تشرینو ڤەرێن/پاییزە/پاییزو وەرتێن/پاییزیا وەرتێنە",
                "تشرینو پەیێن/بارانڤەردانە/گاڤارە/کەلڤەردانە/ناخلقرانە/پاییزو پەیێن/پاییزیا پەیێنە",
                "کانون/گاغان/تاڤارە/چلەیو ڤەرێن/چلەیو قج",
                "چەلە/چلە/چەلییە/چەلەیو پل/چلەی وەرتی/زەمپەریە/زقناوتە/زقناووتە",
                "سباتە/گوجگە/گوژگە/چەلەیو پەیێن/چلەیو پەیێن",
                "ئادار/ئادارە/ئاودار/مارتە",
            ),
            months_short=(
                "نیسانە",
                "گولانە",
                "ھەزیرانە",
                "تەممووزە",
                "کەشکەلون",
                "تەباخە",
                "تشرینو ڤەرێن",
                "تشرینو پەیێن",
                "کانون",
                "چەلە",
                "سباتە",
                "ئادار",
            ),
            weekdays=(
                "شەممە",
                "یەکشەممە",
                "دووشەممە",
                "سێشەممە",
                "چوارشەممە",
                "پێنجشەممە",
                "هەینی",
            ),
            weekdays_short=("شەممە", "یەک", "دوو", "سێ", "چوار", "پێنج", "هەینی"),
            weekdays_min=("ش", "ی", "د", "س", "چ", "پ", "ه"),
        ),
    },
    LocaleId.KMR: {
        "standard": CalendarNames(
            months=(
                "Xakelêwe",
                "Gulan",
                "Cozerdan",
                "Pûşper",
                "Gelawêj",
                "Xermanan",
                "Rezber",
                "Xezelwer",
                "Sermawez",
                "Befranbar",
                "Rêbendan",
                "Reşemê",
            ),
            months_short=(
                "Xak",
                "Gul",
                "Cozerd",
                "Pûşper",
                "Gelawêj",
                "Xerman",
                "Rezber",
                "Xezel",
                "Serma",
                "Befran",
                "Rêbend",
                "Reşem",
            ),
            weekdays=("Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"),
            weekdays_short=("Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"),
            weekdays_min=("Sa", "Su", "Mo", "Tu", "We", "Th", "Fr"),
        ),
        "gelarêzan": CalendarNames(
            months=(
                "Xakelêwe",
                "Gulan",
                "Cozerdan",
                "Pûşper",
                "Gelawêj",
                "Xermanan",
                "Rezber",
                "Gelarêzan",
                "Sermawez",
                "Befranbar",
                "Rêbendan",
                "Reşemê",
            ),
            months_short=(
                "Xak",
                "Gul",
                "Cozerd",
                "Pûşper",
                "Gelawêj",
                "Xerman",
                "Rezber",
                "Gelarêz",
                "Serma",
                "Befran",
                "Rêbend",
                "Reşem",
            ),
            weekdays=("Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"),
            weekdays_short=("Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"),
            weekdays_min=("Sa", "Su", "Mo", "Tu", "We", "Th", "Fr"),
        ),
        "gelarezan": CalendarNames(
            months=(
                "Xakelêwe",
                "Gulan",
                "Cozerdan",
                "Pûşper",
                "Gelawêj",
                "Xermanan",
                "Rezber",
                "Gelarêzan",
                "Sermawez",
                "Befranbar",
                "Rêbendan",
                "Reşemê",
            ),
            months_short=(
                "Xak",
                "Gul",
                "Cozerd",
                "Pûşper",
                "Gelawêj",
                "Xerman",
                "Rezber",
                "Gelarêz",
                "Serma",
                "Befran",
                "Rêbend",
                "Reşem",
            ),
            weekdays=("Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"),
            weekdays_short=("Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"),
            weekdays_min=("Sa", "Su", "Mo", "Tu", "We", "Th", "Fr"),
        ),
        "kmr_wikipedia": CalendarNames(
            months=(
                "Nîsan",
                "Gulan",
                "Hezîran",
                "Tîrmeh",
                "Îlon",
                "Tebax",
                "Cotmeh",
                "Mijdar",
                "Kanûn",
                "Çile",
                "Sibat",
                "Adar",
            ),
            months_short=(
                "Nîs",
                "Gul",
                "Hez",
                "Tîr",
                "Îlo",
                "Teb",
                "Cot",
                "Mij",
                "Kan",
                "Çil",
                "Sib",
                "Ada",
            ),
            weekdays=("Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"),
            weekdays_short=("Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"),
            weekdays_min=("Sa", "Su", "Mo", "Tu", "We", "Th", "Fr"),
        ),
        "zza_zazaki": CalendarNames(
            months=(
                "Nîsanê/Lîzan",
                "Gulanê",
                "Hezîranê/Verên",
                "Temûzê/Tirmeng",
                "Elonê/Payîz",
                "Tebaxê",
                "Tişrînê Verên",
                "Tişrînê Peyên",
                "Kanûn",
                "Çele",
                "Sibatê",
                "Adar",
            ),
            months_short=(
                "Nîsanê",
                "Gulanê",
                "Hezîranê",
                "Temûzê",
                "Elonê",
                "Tebaxê",
                "Tişrîn V.",
                "Tişrîn P.",
                "Kanûn",
                "Çele",
                "Sibatê",
                "Adar",
            ),
            weekdays=("Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"),
            weekdays_short=("Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"),
            weekdays_min=("Sa", "Su", "Mo", "Tu", "We", "Th", "Fr"),
        ),
    },
}
