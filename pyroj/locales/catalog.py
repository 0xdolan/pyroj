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

    def _parse_seq(seq: list[str | list[str]]) -> tuple[tuple[str, ...], ...]:
        res: list[tuple[str, ...]] = []
        for item in seq:
            if isinstance(item, str):
                res.append((item,))
            elif isinstance(item, list):
                res.append(tuple(item))
            else:
                res.append(tuple([str(item)]))
        return tuple(res)

    return CalendarNames(
        months=_parse_seq(d.get("months", [])),
        months_short=_parse_seq(d.get("months_short", [])),
        weekdays=_parse_seq(d.get("weekdays", [])),
        weekdays_short=_parse_seq(d.get("weekdays_short", [])),
        weekdays_min=_parse_seq(d.get("weekdays_min", [])),
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
                ("خاکه‌لێوه", "نەورۆز", "ھەرمێ پشکوان"),
                ("گوڵان",),
                ("جۆزه‌ردان",),
                ("پوشپه‌ر",),
                ("گه‌لاوێژ",),
                ("خه‌رمانان",),
                ("ره‌زبه‌ر",),
                ("گه‌ڵارێزان",),
                ("سه‌رماوه‌ز",),
                ("به‌فرانبار",),
                ("رێبه‌ندان",),
                ("ره‌شه‌مێ",),
            ),
            months_short=(
                ("خاکه",),
                ("گوڵا",),
                ("جۆزه",),
                ("پوشپ",),
                ("گه‌ل",),
                ("خه‌ر",),
                ("ره‌ز",),
                ("گه‌ڵ",),
                ("سه‌ر",),
                ("به‌ف",),
                ("رێبه",),
                ("ره‌ش",),
            ),
            weekdays=(
                ("شەممە",),
                ("یەکشەممە",),
                ("دووشەممە",),
                ("سێشەممە",),
                ("چوارشەممە",),
                ("پێنجشەممە",),
                ("هەینی",),
            ),
            weekdays_short=(
                ("شەممە",),
                ("یەک",),
                ("دوو",),
                ("سێ",),
                ("چوار",),
                ("پێنج",),
                ("هەینی",),
            ),
            weekdays_min=(
                ("ش",),
                ("ی",),
                ("د",),
                ("س",),
                ("چ",),
                ("پ",),
                ("ه",),
            ),
        ),
        "sdh_kelhuri": CalendarNames(
            months=(
                ("جەژنان",),
                ("گوڵان",),
                ("زەردان",),
                ("پەرپەر",),
                ("گه‌لاویژ",),
                ("نوخشان",),
                ("بەران",),
                ("خەزان",),
                ("ساران",),
                ("بەفران",),
                ("بەندان",),
                ("رەمشان",),
            ),
            months_short=(
                ("جەژن",),
                ("گوڵا",),
                ("زەرد",),
                ("پەرپ",),
                ("گه‌ل",),
                ("نوخش",),
                ("بەرا",),
                ("خەزا",),
                ("سارا",),
                ("بەفر",),
                ("بەند",),
                ("رەمش",),
            ),
            weekdays=(
                ("شەممە",),
                ("یەکشەممە",),
                ("دووشەممە",),
                ("سێشەممە",),
                ("چوارشەممە",),
                ("پێنجشەممە",),
                ("هەینی",),
            ),
            weekdays_short=(
                ("شەممە",),
                ("یەک",),
                ("دوو",),
                ("سێ",),
                ("چوار",),
                ("پێنج",),
                ("هەینی",),
            ),
            weekdays_min=(
                ("ش",),
                ("ی",),
                ("د",),
                ("س",),
                ("چ",),
                ("پ",),
                ("ه",),
            ),
        ),
        "lki_laki": CalendarNames(
            months=(
                ("پەنجە",),
                ("میریان",),
                ("گاکووڕ",),
                ("ئاگرانی",),
                ("مردار",),
                ("ماڵەژێر",),
                ("ماڵەژێر دوماینە",),
                ("تۊلتەکن",),
                ("مانگ سیە",),
                ("نۆڕووژ",),
                ("خاکەلیە",),
                ("مانگ لیە",),
            ),
            months_short=(
                ("پەنج",),
                ("میری",),
                ("گاکو",),
                ("ئاگر",),
                ("مردا",),
                ("ماڵە",),
                ("ماڵە",),
                ("تۊلت",),
                ("مانگ",),
                ("نۆڕو",),
                ("خاکە",),
                ("مانگ",),
            ),
            weekdays=(
                ("شەممە",),
                ("یەکشەممە",),
                ("دووشەممە",),
                ("سێشەممە",),
                ("چوارشەممە",),
                ("پێنجشەممە",),
                ("هەینی",),
            ),
            weekdays_short=(
                ("شەممە",),
                ("یەک",),
                ("دوو",),
                ("سێ",),
                ("چوار",),
                ("پێنج",),
                ("هەینی",),
            ),
            weekdays_min=(
                ("ش",),
                ("ی",),
                ("د",),
                ("س",),
                ("چ",),
                ("پ",),
                ("ه",),
            ),
        ),
        "hac_hawrami": CalendarNames(
            months=(
                ("نەوڕۆز",),
                ("پاژەرەژ",),
                ("چێڵکڕ",),
                ("کۆپڕ",),
                ("گه‌لاوێژ",),
                ("ئاوەوەرە",),
                ("ترازیێ",),
                ("گه‌ڵاخەزان",),
                ("کەڵەھەرز",),
                ("ئارگا",),
                ("رابڕان",),
                ("سیاوکام",),
            ),
            months_short=(
                ("نەوڕ",),
                ("پاژە",),
                ("چێڵک",),
                ("کۆپڕ",),
                ("گه‌ل",),
                ("ئاوە",),
                ("تراز",),
                ("گه‌ڵ",),
                ("کەڵە",),
                ("ئارگ",),
                ("رابڕ",),
                ("سیاو",),
            ),
            weekdays=(
                ("شەممە",),
                ("یەکشەممە",),
                ("دووشەممە",),
                ("سێشەممە",),
                ("چوارشەممە",),
                ("پێنجشەممە",),
                ("هەینی",),
            ),
            weekdays_short=(
                ("شەممە",),
                ("یەک",),
                ("دوو",),
                ("سێ",),
                ("چوار",),
                ("پێنج",),
                ("هەینی",),
            ),
            weekdays_min=(
                ("ش",),
                ("ی",),
                ("د",),
                ("س",),
                ("چ",),
                ("پ",),
                ("ه",),
            ),
        ),
        "zza_zazaki": CalendarNames(
            months=(
                ("نیسانە",),
                ("گولانە",),
                ("ھەزیرانە", "ڤارتڤارە", "ئامنانو ڤەرێن", "ئامنانیا ڤەرێنە"),
                ("تەممووزە",),
                ("تەباخە", "ئامنانو پەیێن", "ئامنانیا پەیێنە", "ئاگوستە"),
                (
                    "کەشکەلون",
                    "جتمەنگی",
                    "ئێلولە",
                    "ئەلون",
                    "ئیلۆنە",
                    "پاییزو ڤەرێن",
                    "پاییزیا ڤەرێنە",
                ),
                ("تشرینو ڤەرێن", "پاییزە", "پاییزو وەرتێن", "پاییزیا وەرتێنە"),
                (
                    "تشرینو پەیێن",
                    "بارانڤەردانە",
                    "گاڤارە",
                    "کەلڤەردانە",
                    "ناخلقرانە",
                    "پاییزو پەیێن",
                    "پاییزیا پەیێنە",
                ),
                (
                    "تشرینو پەیێن",
                    "بارانڤەردانە",
                    "گاڤارە",
                    "کەلڤەردانە",
                    "ناخلقرانە",
                    "پاییزو پەیێن",
                    "پاییزیا پەیێنە",
                ),
                (
                    "چلە",
                    "چلە",
                    "چەلییە",
                    "چەلەیو پل",
                    "چلەی وەرتی",
                    "زەمپەریە",
                    "زقناوتە",
                    "زقناووتە",
                ),
                ("سباتە", "گوجگە", "گوژگە", "چەڵەیو پەیێن", "چلەیو پەیێن"),
                ("ئادار", "ئادارە", "ئاودار", "مارتە"),
            ),
            months_short=(
                ("نیسا",),
                ("گولا",),
                ("ھەزی",),
                ("تەمم",),
                ("تەبا",),
                ("کەشک",),
                ("تشری",),
                ("تشری",),
                ("تشری",),
                ("چلە",),
                ("سبات",),
                ("ئادا",),
            ),
            weekdays=(
                ("شەممە",),
                ("یەکشەممە",),
                ("دووشەممە",),
                ("سێشەممە",),
                ("چوارشەممە",),
                ("پێنجشەممە",),
                ("هەینی",),
            ),
            weekdays_short=(
                ("شەممە",),
                ("یەک",),
                ("دوو",),
                ("سێ",),
                ("چوار",),
                ("پێنج",),
                ("هەینی",),
            ),
            weekdays_min=(
                ("ش",),
                ("ی",),
                ("د",),
                ("س",),
                ("چ",),
                ("پ",),
                ("ه",),
            ),
        ),
        "syriac": CalendarNames(
            months=(
                ("کانوونی دووه‌م",),
                ("شوبات",),
                ("ئازار",),
                ("نیسان",),
                ("ئایار",),
                ("حوزەیران",),
                ("تەممووز",),
                ("ئاب",),
                ("کانون",),
                ("تشرینی یەکەم",),
                ("تشرینی دووه‌م",),
                ("کانوونی یەکەم",),
            ),
            months_short=(
                ("کانو",),
                ("شوبا",),
                ("ئازا",),
                ("نیسا",),
                ("ئایا",),
                ("حوزە",),
                ("تەمم",),
                ("ئاب",),
                ("کانو",),
                ("تشری",),
                ("تشری",),
                ("کانو",),
            ),
            weekdays=(
                ("شەممە",),
                ("یەکشەممە",),
                ("دووشەممە",),
                ("سێشەممە",),
                ("چوارشەممە",),
                ("پێنجشەممە",),
                ("هەینی",),
            ),
            weekdays_short=(
                ("شەممە",),
                ("یەک",),
                ("دوو",),
                ("سێ",),
                ("چوار",),
                ("پێنج",),
                ("هەینی",),
            ),
            weekdays_min=(
                ("ش",),
                ("ی",),
                ("د",),
                ("س",),
                ("چ",),
                ("پ",),
                ("ه",),
            ),
        ),
    },
    LocaleId.KMR: {
        "standard": CalendarNames(
            months=(
                ("Nîsan", "Newroz", "Herme Pişkewan"),
                ("Gulan",),
                ("Hezîran",),
                ("Tîrmeh",),
                ("Gelawêj",),
                ("Îlon",),
                ("Rezber",),
                ("Gellarêzan",),
                ("Sermawez",),
                ("Befranbar",),
                ("Rêbendan",),
                ("Reşemê",),
            ),
            months_short=(
                ("Nîsa",),
                ("Gula",),
                ("Hezî",),
                ("Tîrm",),
                ("Gela",),
                ("Îlon",),
                ("Rezb",),
                ("Gell",),
                ("Serm",),
                ("Befr",),
                ("Rêbe",),
                ("Reşe",),
            ),
            weekdays=(
                ("Saturday",),
                ("Sunday",),
                ("Monday",),
                ("Tuesday",),
                ("Wednesday",),
                ("Thursday",),
                ("Friday",),
            ),
            weekdays_short=(
                ("Sat",),
                ("Sun",),
                ("Mon",),
                ("Tue",),
                ("Wed",),
                ("Thu",),
                ("Fri",),
            ),
            weekdays_min=(
                ("Sa",),
                ("Su",),
                ("Mo",),
                ("Tu",),
                ("We",),
                ("Th",),
                ("Fr",),
            ),
        ),
        "sdh_kelhuri": CalendarNames(
            months=(
                ("Cejnan",),
                ("Gulan",),
                ("Zerdan",),
                ("Perper",),
                ("Gelawêj",),
                ("Noxşan",),
                ("Beran",),
                ("Xezan",),
                ("Saran",),
                ("Befran",),
                ("Bendan",),
                ("Remşan",),
            ),
            months_short=(
                ("Cejn",),
                ("Gula",),
                ("Zerd",),
                ("Perp",),
                ("Gela",),
                ("Noxş",),
                ("Bera",),
                ("Xeza",),
                ("Sara",),
                ("Befr",),
                ("Bend",),
                ("Remş",),
            ),
            weekdays=(
                ("Saturday",),
                ("Sunday",),
                ("Monday",),
                ("Tuesday",),
                ("Wednesday",),
                ("Thursday",),
                ("Friday",),
            ),
            weekdays_short=(
                ("Sat",),
                ("Sun",),
                ("Mon",),
                ("Tue",),
                ("Wed",),
                ("Thu",),
                ("Fri",),
            ),
            weekdays_min=(
                ("Sa",),
                ("Su",),
                ("Mo",),
                ("Tu",),
                ("We",),
                ("Th",),
                ("Fr",),
            ),
        ),
        "lki_laki": CalendarNames(
            months=(
                ("Pence",),
                ("Miryan",),
                ("Gakûr",),
                ("Agranî",),
                ("Mirdar",),
                ("Malajêr",),
                ("Malajêr 2",),
                ("Tultek",),
                ("Mang Sî",),
                ("Norûj",),
                ("Xakelî",),
                ("Mang Lî",),
            ),
            months_short=(
                ("Penc",),
                ("Miry",),
                ("Gakû",),
                ("Agra",),
                ("Mird",),
                ("Mala",),
                ("Mala",),
                ("Tult",),
                ("Mang",),
                ("Norû",),
                ("Xake",),
                ("Mang",),
            ),
            weekdays=(
                ("Saturday",),
                ("Sunday",),
                ("Monday",),
                ("Tuesday",),
                ("Wednesday",),
                ("Thursday",),
                ("Friday",),
            ),
            weekdays_short=(
                ("Sat",),
                ("Sun",),
                ("Mon",),
                ("Tue",),
                ("Wed",),
                ("Thu",),
                ("Fri",),
            ),
            weekdays_min=(
                ("Sa",),
                ("Su",),
                ("Mo",),
                ("Tu",),
                ("We",),
                ("Th",),
                ("Fr",),
            ),
        ),
        "hac_hawrami": CalendarNames(
            months=(
                ("Newroz",),
                ("Pajerej",),
                ("Çêlkr",),
                ("Kopr",),
                ("Gelawêj",),
                ("Awewere",),
                ("Terazî",),
                ("Gelaxezan",),
                ("Keleherz",),
                ("Arga",),
                ("Rabran",),
                ("Siyawkam",),
            ),
            months_short=(
                ("Newr",),
                ("Paje",),
                ("Çêlk",),
                ("Kopr",),
                ("Gela",),
                ("Awew",),
                ("Tera",),
                ("Gela",),
                ("Kele",),
                ("Arga",),
                ("Rabr",),
                ("Siya",),
            ),
            weekdays=(
                ("Saturday",),
                ("Sunday",),
                ("Monday",),
                ("Tuesday",),
                ("Wednesday",),
                ("Thursday",),
                ("Friday",),
            ),
            weekdays_short=(
                ("Sat",),
                ("Sun",),
                ("Mon",),
                ("Tue",),
                ("Wed",),
                ("Thu",),
                ("Fri",),
            ),
            weekdays_min=(
                ("Sa",),
                ("Su",),
                ("Mo",),
                ("Tu",),
                ("We",),
                ("Th",),
                ("Fr",),
            ),
        ),
        "zza_zazaki": CalendarNames(
            months=(
                ("Nîsan",),
                ("Gulan",),
                ("Hezîran", "Vartvar", "Amano Verên", "Amaniya Verêne"),
                ("Temmuz",),
                ("Tebax", "Amano Peyên", "Amaniya Peyêne", "Awuste"),
                (
                    "Keshkelon",
                    "Ctemengi",
                    "Îlule",
                    "Elon",
                    "Îlonê",
                    "Payîzo Verên",
                    "Payîzya Verêne",
                ),
                ("Tişrino Verên", "Payîza", "Payîzo Werten", "Payîzya Wertenê"),
                (
                    "Tişrino Peyên",
                    "Baranverdene",
                    "Gavare",
                    "Kelverde",
                    "Naxelqerane",
                    "Payîzo Peyên",
                    "Payîzya Peyêne",
                ),
                (
                    "Tişrino Peyên",
                    "Baranverdene",
                    "Gavare",
                    "Kelverde",
                    "Naxelqerane",
                    "Payîzo Peyên",
                    "Payîzya Peyêne",
                ),
                (
                    "Çile",
                    "Çile",
                    "Çêliye",
                    "Çileyo Pel",
                    "Çiley Werti",
                    "Zemperî",
                    "Zqnewte",
                    "Zqnewte",
                ),
                ("Sibat", "Gujge", "Gujge", "Çileyo Peyên", "Çileyo Peyên"),
                ("Adar", "Adare", "Audar", "Marte"),
            ),
            months_short=(
                ("Nîsa",),
                ("Gula",),
                ("Hezî",),
                ("Temm",),
                ("Teba",),
                ("Kesh",),
                ("Tişr",),
                ("Tişr",),
                ("Tişr",),
                ("Çile",),
                ("Siba",),
                ("Adar",),
            ),
            weekdays=(
                ("Saturday",),
                ("Sunday",),
                ("Monday",),
                ("Tuesday",),
                ("Wednesday",),
                ("Thursday",),
                ("Friday",),
            ),
            weekdays_short=(
                ("Sat",),
                ("Sun",),
                ("Mon",),
                ("Tue",),
                ("Wed",),
                ("Thu",),
                ("Fri",),
            ),
            weekdays_min=(
                ("Sa",),
                ("Su",),
                ("Mo",),
                ("Tu",),
                ("We",),
                ("Th",),
                ("Fr",),
            ),
        ),
        "syriac": CalendarNames(
            months=(
                ("Kanûnê Duyem",),
                ("Şubat",),
                ("Adar",),
                ("Nîsan",),
                ("Gulan",),
                ("Hezîran",),
                ("Tîrmeh",),
                ("Tebax",),
                ("Kanûn",),
                ("Tişrîn 1",),
                ("Tişrîn 2",),
                ("Kanûnê Yekem",),
            ),
            months_short=(
                ("Kanû",),
                ("Şuba",),
                ("Adar",),
                ("Nîsa",),
                ("Gula",),
                ("Hezî",),
                ("Tîrm",),
                ("Teba",),
                ("Kanû",),
                ("Tişr",),
                ("Tişr",),
                ("Kanû",),
            ),
            weekdays=(
                ("Saturday",),
                ("Sunday",),
                ("Monday",),
                ("Tuesday",),
                ("Wednesday",),
                ("Thursday",),
                ("Friday",),
            ),
            weekdays_short=(
                ("Sat",),
                ("Sun",),
                ("Mon",),
                ("Tue",),
                ("Wed",),
                ("Thu",),
                ("Fri",),
            ),
            weekdays_min=(
                ("Sa",),
                ("Su",),
                ("Mo",),
                ("Tu",),
                ("We",),
                ("Th",),
                ("Fr",),
            ),
        ),
    },
}
