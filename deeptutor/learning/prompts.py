"""Mastery Path LLM prompt templates (Optimized for Vietnamese)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from deeptutor.services.prompt.language import append_language_directive, normalize_language

_PROMPT_DIR = Path(__file__).with_name("prompts")


def _get_nested(data: dict[str, Any], path: str, default: str = "") -> str:
    value: Any = data
    for part in path.split("."):
        if not isinstance(value, dict):
            return default
        value = value.get(part)
    return value if isinstance(value, str) else default


@lru_cache(maxsize=8)
def get_learning_prompts(language: str = "vi") -> dict[str, Any]:
    """Load localized Mastery Path LLM prompts (defaults to Vietnamese)."""
    lang = normalize_language(language)
    candidates = dict.fromkeys([lang, lang.split("-", 1)[0], "vi", "en"])
    for candidate in candidates:
        path = _PROMPT_DIR / f"{candidate}.yaml"
        if path.exists():
            return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {}


def prompt_text(language: str, path: str, default: str = "") -> str:
    return _get_nested(get_learning_prompts(language), path, default)


def notebook_generation_prompts(language: str, records_json: str) -> tuple[str, str]:
    lang = normalize_language(language)
    prompts = get_learning_prompts(lang)
    system_prompt = _get_nested(prompts, "notebook.system", NOTEBOOK_SYSTEM)
    user_template = _get_nested(prompts, "notebook.user", NOTEBOOK_USER)
    system_prompt = append_language_directive(system_prompt, lang)
    return system_prompt, user_template.format(records_json=records_json)


_MUST_COVER_HEADERS = {
    "vi": "Phiên bản lộ trình trước đã bỏ sót các tài liệu sau, phiên bản này BẮT BUỘC phải đưa đầy đủ từng tài liệu vào chương học phù hợp:",
    "en": (
        "The previous route left these documents out. This one must give every "
        "single one of them a place:"
    ),
}


def _must_cover_block(language: str, must_cover: list[str]) -> str:
    if not must_cover:
        return ""
    lang = normalize_language(language)
    header = _MUST_COVER_HEADERS["vi" if lang.startswith("vi") else "en"]
    listed = "\n".join(f"- {name}" for name in must_cover[:40])
    return f"\n{header}\n{listed}\n"


def topic_generation_prompts(
    language: str,
    *,
    name: str,
    goal: str,
    sources_json: str,
    module_limit: int = 8,
    must_cover: list[str] | None = None,
) -> tuple[str, str]:
    lang = normalize_language(language)
    prompts = get_learning_prompts(lang)
    system_prompt = _get_nested(
        prompts,
        "topic.system",
        "Bạn là kiến trúc sư chương trình học Mastery Learning. Chỉ trả về JSON với nội dung Tiếng Việt tự nhiên.",
    )
    user_template = _get_nested(
        prompts,
        "topic.user",
        "Thiết kế lộ trình học cho {name}: {goal}. Nguồn: {sources_json}",
    )
    system_prompt = append_language_directive(system_prompt, lang)
    system_prompt = system_prompt.replace("{module_limit}", str(max(3, int(module_limit or 8))))
    return system_prompt, user_template.format(
        name=name,
        goal=goal,
        sources_json=sources_json,
        must_cover_block=_must_cover_block(lang, must_cover or []),
    )


def default_module_name(language: str, index: int) -> str:
    template = prompt_text(language, "notebook.default_module_name", "Chương {index}")
    return template.format(index=index)


DIAGNOSTIC_SYSTEM = prompt_text("vi", "diagnostic.system")
DIAGNOSTIC_USER = prompt_text("vi", "diagnostic.user")
EXPLAIN_SYSTEM = prompt_text("vi", "explain.system")
EXPLAIN_USER = prompt_text("vi", "explain.user")
FEYNMAN_SYSTEM = prompt_text("vi", "feynman.system")
FEYNMAN_USER = prompt_text("vi", "feynman.user")
PRACTICE_SYSTEM = prompt_text("vi", "practice.system")
PRACTICE_USER = prompt_text("vi", "practice.user")
ERROR_DIAGNOSIS_SYSTEM = prompt_text("vi", "error_diagnosis.system")
ERROR_DIAGNOSIS_USER = prompt_text("vi", "error_diagnosis.user")
REVIEW_SYSTEM = prompt_text("vi", "review.system")
REVIEW_USER = prompt_text("vi", "review.user")
NOTEBOOK_SYSTEM = prompt_text("vi", "notebook.system")
NOTEBOOK_USER = prompt_text("vi", "notebook.user")


__all__ = [
    "DIAGNOSTIC_SYSTEM",
    "DIAGNOSTIC_USER",
    "ERROR_DIAGNOSIS_SYSTEM",
    "ERROR_DIAGNOSIS_USER",
    "EXPLAIN_SYSTEM",
    "EXPLAIN_USER",
    "FEYNMAN_SYSTEM",
    "FEYNMAN_USER",
    "NOTEBOOK_SYSTEM",
    "NOTEBOOK_USER",
    "PRACTICE_SYSTEM",
    "PRACTICE_USER",
    "REVIEW_SYSTEM",
    "REVIEW_USER",
    "default_module_name",
    "get_learning_prompts",
    "notebook_generation_prompts",
    "prompt_text",
    "topic_generation_prompts",
]
