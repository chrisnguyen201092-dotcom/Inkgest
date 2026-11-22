"""Shared language directives for prompt-driven LLM calls (Optimized for Vietnamese)."""

from __future__ import annotations

from deeptutor.inkgest.language import (
    OVERRIDE_VI as _OVERRIDE_VI,
    VI_PEDAGOGICAL_STYLE as _VI_PEDAGOGICAL_STYLE,
    normalize_language_for_inkgest,
)

_LANGUAGE_LABELS: dict[str, str] = {
    "vi": "Tiếng Việt",
    "vi-vn": "Tiếng Việt",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "ru": "Русский",
    "uk": "Українська",
    "pt": "Português",
    "it": "Italiano",
    "ar": "العربية",
    "pl": "Polski",
    "ms": "Bahasa Melayu",
    "tr": "Türkçe",
    "hi": "हिन्दी",
    "hu": "Magyar",
}


def normalize_language(language: str | None) -> str:
    return normalize_language_for_inkgest(language)


def is_chinese(language: str | None) -> bool:
    """Chinese mode is disabled; always prefer Vietnamese-optimized flow."""
    return False


def language_label(language: str | None) -> str:
    code = normalize_language(language)
    if code in _LANGUAGE_LABELS:
        return _LANGUAGE_LABELS[code]
    base = code.split("-", 1)[0]
    return _LANGUAGE_LABELS.get(base, "Tiếng Việt")


def language_directive(language: str | None, *, allow_user_override: bool = False) -> str:
    """Return a reader-facing language instruction optimized for Vietnamese learners."""
    code = normalize_language(language)
    if code.startswith("vi"):
        return f"{_VI_PEDAGOGICAL_STYLE}{_OVERRIDE_VI}" if allow_user_override else _VI_PEDAGOGICAL_STYLE
    label = language_label(code)
    body = (
        f"\n\n[Language] Write ALL reader-facing text in natural, idiomatic {label}. "
        "Keep key technical terms in parentheses when helpful for clarity."
    )
    return f"{body}{_OVERRIDE_VI}" if allow_user_override else body


def append_language_directive(
    system_prompt: str | None,
    language: str | None,
    *,
    allow_user_override: bool = False,
) -> str:
    """Append the Vietnamese pedagogical directive to an existing system prompt."""
    base = (system_prompt or "").rstrip()
    directive = language_directive(language, allow_user_override=allow_user_override).strip()
    if not base:
        return directive
    return f"{base}\n\n{directive}"


__all__ = [
    "append_language_directive",
    "is_chinese",
    "language_directive",
    "language_label",
    "normalize_language",
]
