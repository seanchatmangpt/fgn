from __future__ import annotations

import re
import unicodedata
from typing import Any

from jinja2.ext import Extension

try:
    import inflection as _inflection
except ImportError:
    _inflection = None


def _transliterate(value: Any) -> str:
    return unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")


def _underscore(value: Any) -> str:
    text = str(value).replace("::", "/")
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", text)
    return text.replace("-", "_").lower()


def _camelize(value: Any) -> str:
    return "".join(part[:1].upper() + part[1:] for part in _underscore(value).split("_") if part)


def _dasherize(value: Any) -> str:
    return str(value).replace("_", "-")


def _humanize(value: Any) -> str:
    text = re.sub(r"_id$", "", _underscore(value)).replace("_", " ")
    return text[:1].upper() + text[1:]


def _ordinal(value: Any) -> str:
    number = int(value)
    if 10 <= number % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")


def _ordinalize(value: Any) -> str:
    return f"{value}{_ordinal(value)}"


def _parameterize(value: Any, separator: str = "-") -> str:
    text = _transliterate(value).lower()
    text = re.sub(r"[^a-z0-9]+", separator, text)
    return text.strip(separator)


def _pluralize(value: Any) -> str:
    word = str(value)
    irregular = {"child": "children", "person": "people", "man": "men", "woman": "women"}
    if word.lower() in irregular:
        result = irregular[word.lower()]
        return result.capitalize() if word[:1].isupper() else result
    if re.search(r"[^aeiou]y$", word, re.IGNORECASE):
        return word[:-1] + "ies"
    if re.search(r"(s|x|z|ch|sh)$", word, re.IGNORECASE):
        return word + "es"
    return word if word.endswith("s") else word + "s"


def _singularize(value: Any) -> str:
    word = str(value)
    irregular = {"children": "child", "people": "person", "men": "man", "women": "woman"}
    if word.lower() in irregular:
        result = irregular[word.lower()]
        return result.capitalize() if word[:1].isupper() else result
    if re.search(r"ies$", word, re.IGNORECASE):
        return word[:-3] + "y"
    if re.search(r"(ches|shes|xes|zes)$", word, re.IGNORECASE):
        return word[:-2]
    return word[:-1] if word.endswith("s") else word


def _tableize(value: Any) -> str:
    return _pluralize(_underscore(value))


def _titleize(value: Any) -> str:
    return _humanize(value).title()


_FALLBACKS = {
    "camelize": _camelize,
    "dasherize": _dasherize,
    "humanize": _humanize,
    "ordinal": _ordinal,
    "ordinalize": _ordinalize,
    "parameterize": _parameterize,
    "pluralize": _pluralize,
    "singularize": _singularize,
    "tableize": _tableize,
    "titleize": _titleize,
    "transliterate": _transliterate,
    "underscore": _underscore,
}


class InflectionExtension(Extension):
    """Expose inflection filters with a dependency-free compatibility fallback."""

    def __init__(self, environment):
        super().__init__(environment)
        for name, fallback in _FALLBACKS.items():
            environment.filters[name] = (
                getattr(_inflection, name) if _inflection is not None else fallback
            )
