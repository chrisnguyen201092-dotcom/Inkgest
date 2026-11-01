"""Source-grounded vocabulary help for Immersive Reading."""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from deeptutor.reading._grounding import grounded_prompt as _prompt
from deeptutor.reading.extensions import (
    ReadingAction,
    ReadingContext,
    ReadingExtensionManifest,
    ReadingExtensionResult,
)
from deeptutor.services.llm import complete
from deeptutor.services.llm.structured_retry import json_with_reasoning_retry
from deeptutor.services.prompt.language import append_language_directive, is_chinese as _is_zh

_SYSTEM_VI = """Bạn giải thích các thuật ngữ / từ vựng quan trọng xuất hiện trong đoạn văn vừa chọn bằng Tiếng Việt tự nhiên, dễ hiểu.

Chỉ dựa vào đoạn trích và ngữ cảnh xung quanh.

Chỉ trả về JSON: {"terms":[{"term":"từ/cụm từ nguyên văn trong đoạn chọn","meaning":"giải nghĩa bản chất bằng Tiếng Việt tự nhiên, thoát ý","usage":"cách thuật ngữ này được vận dụng trong ngữ cảnh đoạn văn"}]}.
Chọn từ 1 đến 5 thuật ngữ quan trọng nhất giúp người đọc hiểu nhanh đoạn văn. Lưu ý: trường term PHẢI giữ nguyên văn như trong đoạn trích, còn meaning và usage viết bằng Tiếng Việt mạch lạc, dễ nhớ.
"""

_SYSTEM_EN = _SYSTEM_VI
_SYSTEM_ZH = _SYSTEM_VI


class _VocabularyTerm(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    term: str = Field(min_length=2, max_length=80)
    meaning: str = Field(min_length=8, max_length=600)
    usage: str = Field(min_length=8, max_length=600)


class _Vocabulary(BaseModel):
    model_config = ConfigDict(extra="ignore")

    terms: list[_VocabularyTerm] = Field(min_length=1, max_length=5)

    @field_validator("terms")
    @classmethod
    def validate_terms(cls, value: list[_VocabularyTerm]) -> list[_VocabularyTerm]:
        normalized = [_normalise(term.term) for term in value]
        if len(set(normalized)) != len(normalized):
            raise ValueError("Vocabulary terms must be unique.")
        return value


def _normalise(value: str) -> str:
    return " ".join(value.casefold().split())


def _term_comes_from_selection(term: str, selection: str) -> bool:
    normalized_term = _normalise(term)
    normalized_selection = _normalise(selection)
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9' -]*", normalized_term):
        pattern = rf"(?<!\w){re.escape(normalized_term)}(?!\w)"
        return re.search(pattern, normalized_selection) is not None
    return normalized_term in normalized_selection


def _vocabulary(data: Any, selection: str) -> _Vocabulary:
    if not isinstance(data, dict) or not data:
        raise ValueError("Vocabulary model returned invalid JSON.")
    try:
        vocabulary = _Vocabulary.model_validate({"terms": data.get("terms")})
    except ValidationError as exc:
        raise ValueError("Vocabulary model returned an invalid shape.") from exc

    if any(not _term_comes_from_selection(term.term, selection) for term in vocabulary.terms):
        raise ValueError("Vocabulary terms must come from the selection.")
    return vocabulary


class VocabularyExtension:
    """Return bounded vocabulary explanations grounded in selected text."""

    manifest = ReadingExtensionManifest(
        id="vocabulary",
        version="1.0.0",
        name="Vocabulary help",
        actions=[
            ReadingAction(id="explain", label="Explain vocabulary", requires=["selection"]),
        ],
        result_types=["card"],
    )

    async def run_action(self, action: str, context: ReadingContext) -> ReadingExtensionResult:
        if action != "explain":
            raise ValueError(f"Unsupported vocabulary action: {action}")
        if not context.selection.strip():
            raise ValueError("Vocabulary help requires selected text.")

        from deeptutor.services.model_selection.tasks import TaskKind, task_llm_scope

        async def _run(reasoning_effort: str | None) -> str:
            return await complete(
                prompt=_prompt(context),
                system_prompt=append_language_directive(
                    _SYSTEM_ZH if _is_zh(context.locale) else _SYSTEM_EN, context.locale
                ),
                temperature=0.2,
                max_tokens=2_000,
                max_retries=0,
                response_format={"type": "json_object"},
                reasoning_effort=reasoning_effort,
            )

        with task_llm_scope(TaskKind.READING_VOCABULARY):
            data = await json_with_reasoning_retry(_run, expected_key="terms")
        vocabulary = _vocabulary(data, context.selection)
        return ReadingExtensionResult(
            type="card",
            title="词汇帮助" if _is_zh(context.locale) else "Vocabulary help",
            message="Explanations use the selected passage."
            if not _is_zh(context.locale)
            else "释义基于所选段落。",
            payload={"terms": [term.model_dump() for term in vocabulary.terms]},
        )


__all__ = ["VocabularyExtension"]
