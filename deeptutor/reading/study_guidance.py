"""Source-grounded study guidance for Immersive Reading."""

from __future__ import annotations

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

_SYSTEM_VI = """Bạn là gia sư hướng dẫn đọc hiểu chuyên sâu. Hãy thiết kế 3 bước tư duy ngắn gọn bằng Tiếng Việt tự nhiên giúp người học nắm bắt nhanh nhất đoạn văn vừa chọn.

Chỉ sử dụng nội dung đoạn trích và ngữ cảnh xung quanh trong tài liệu; không tự bịa thêm định nghĩa hay số trang bên ngoài.

Chỉ trả về JSON: {"focus":"1 câu Tiếng Việt tóm tắt trọng tâm cốt lõi của đoạn này","steps":["Bước 1: ...","Bước 2: ...","Bước 3: ..."]}.
Mỗi bước hướng dẫn người học thực hiện một thao tác tư duy cụ thể trên đoạn văn: từ nhận diện luận điểm chính, liên hệ cơ chế hoạt động, đến tự diễn đạt lại bản chất bằng lời của mình. Viết Tiếng Việt thoát ý, giữ thuật ngữ tiếng Anh trong ngoặc đơn khi cần.
"""

_SYSTEM_EN = _SYSTEM_VI
_SYSTEM_ZH = _SYSTEM_VI


class _Guidance(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    focus: str = Field(min_length=8, max_length=600)
    steps: list[str] = Field(min_length=3, max_length=3)

    @field_validator("steps")
    @classmethod
    def validate_steps(cls, value: list[str]) -> list[str]:
        if any(not 8 <= len(step) <= 500 for step in value):
            raise ValueError("Each study-guidance step must contain 8 to 500 characters.")
        return value


def _guidance(data: Any) -> _Guidance:
    if not isinstance(data, dict) or not data:
        raise ValueError("Study guidance model returned invalid JSON.")
    try:
        return _Guidance.model_validate({"focus": data.get("focus"), "steps": data.get("steps")})
    except ValidationError as exc:
        raise ValueError("Study guidance model returned an invalid shape.") from exc


class StudyGuidanceExtension:
    """Return bounded guidance grounded in the learner's selected text."""

    manifest = ReadingExtensionManifest(
        id="guided_learning",
        version="1.0.0",
        name="Study guidance",
        actions=[
            ReadingAction(id="guide", label="Guide me", requires=["selection"]),
        ],
        result_types=["card"],
    )

    async def run_action(self, action: str, context: ReadingContext) -> ReadingExtensionResult:
        if action != "guide":
            raise ValueError(f"Unsupported study-guidance action: {action}")
        if not context.selection.strip():
            raise ValueError("Study guidance requires selected text.")

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

        with task_llm_scope(TaskKind.READING_GUIDANCE):
            data = await json_with_reasoning_retry(_run, expected_key="steps")
        guidance = _guidance(data)
        return ReadingExtensionResult(
            type="card",
            title="学习引导" if _is_zh(context.locale) else "Study guidance",
            message=guidance.focus,
            payload={"steps": guidance.steps},
        )


__all__ = ["StudyGuidanceExtension"]
