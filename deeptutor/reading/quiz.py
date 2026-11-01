"""Source-grounded quiz generation for Immersive Reading."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from deeptutor.reading._grounding import evidence_key
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

_SYSTEM_VI = """Bạn biên soạn một bài trắc nghiệm ngắn bằng Tiếng Việt tự nhiên để kiểm tra mức độ hiểu sâu đoạn văn đang đọc.

Chỉ dựa trên ngữ cảnh tài liệu được cung cấp, không bịa thêm thông tin bên ngoài.

Chỉ trả về JSON: {"questions":[{"prompt":"Câu hỏi bằng Tiếng Việt tự nhiên, rõ nghĩa","choices":["Phương án A","Phương án B","Phương án C","Phương án D"],"correct_choice_index":0,"evidence":"cụm từ nguyên văn trong tài liệu chứng minh đáp án đúng"}]}.
Trả về đúng 3 câu hỏi. Mỗi câu có 4 phương án khác biệt và 1 đáp án đúng nhất (correct_choice_index tính từ 0). Lưu ý: trường evidence PHẢI trích nguyên văn (exact substring) từ văn bản gốc để hệ thống đối chiếu tự động, còn prompt và choices viết bằng Tiếng Việt tự nhiên (kèm thuật ngữ gốc trong ngoặc nếu cần).
"""

_SYSTEM_EN = _SYSTEM_VI
_SYSTEM_ZH = _SYSTEM_VI


class _QuizQuestion(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    prompt: str = Field(min_length=12, max_length=600)
    choices: list[str] = Field(min_length=4, max_length=4)
    correct_choice_index: int = Field(ge=0, le=3)
    evidence: str = Field(min_length=8, max_length=600)

    @field_validator("choices")
    @classmethod
    def validate_choices(cls, value: list[str]) -> list[str]:
        if any(not 2 <= len(choice) <= 240 for choice in value):
            raise ValueError("Each quiz choice must contain 2 to 240 characters.")
        normalized = [_normalise(choice) for choice in value]
        if len(set(normalized)) != len(normalized):
            raise ValueError("Quiz choices must be unique.")
        return value


class _Quiz(BaseModel):
    model_config = ConfigDict(extra="ignore")

    questions: list[_QuizQuestion] = Field(min_length=3, max_length=3)


def _normalise(value: str) -> str:
    return " ".join(value.casefold().split())


def _quiz(data: Any, context: ReadingContext) -> _Quiz:
    if not isinstance(data, dict) or not data:
        raise ValueError("Reading quiz model returned invalid JSON.")
    try:
        quiz = _Quiz.model_validate({"questions": data.get("questions")})
    except ValidationError as exc:
        raise ValueError("Reading quiz model returned an invalid shape.") from exc

    context_key = evidence_key(context.visible_text)
    if any(evidence_key(question.evidence) not in context_key for question in quiz.questions):
        raise ValueError("Reading quiz evidence must come from the reading context.")
    return quiz


class ReadingQuizExtension:
    """Return bounded comprehension questions grounded in the current unit."""

    manifest = ReadingExtensionManifest(
        id="quiz",
        version="1.0.0",
        name="Reading quiz",
        actions=[
            ReadingAction(id="start", label="Quiz me", requires=["visible_text"]),
        ],
        result_types=["quiz"],
    )

    async def run_action(self, action: str, context: ReadingContext) -> ReadingExtensionResult:
        if action != "start":
            raise ValueError(f"Unsupported reading-quiz action: {action}")
        if not context.visible_text.strip():
            raise ValueError("Reading quiz requires visible text.")

        from deeptutor.services.model_selection.tasks import TaskKind, task_llm_scope

        async def _run(reasoning_effort: str | None) -> str:
            return await complete(
                prompt=_prompt(context),
                system_prompt=append_language_directive(
                    _SYSTEM_ZH if _is_zh(context.locale) else _SYSTEM_EN, context.locale
                ),
                temperature=0.3,
                max_tokens=2_500,
                max_retries=0,
                response_format={"type": "json_object"},
                reasoning_effort=reasoning_effort,
            )

        with task_llm_scope(TaskKind.READING_QUIZ):
            data = await json_with_reasoning_retry(
                _run,
                expected_key="questions",
            )
        quiz = _quiz(data, context)
        return ReadingExtensionResult(
            type="quiz",
            title="阅读测验" if _is_zh(context.locale) else "Reading quiz",
            message="Questions use the current passage."
            if not _is_zh(context.locale)
            else "题目基于当前段落。",
            payload={
                "questions": [
                    {
                        "id": f"q_{index}",
                        "prompt": question.prompt,
                        "choices": question.choices,
                        "correct_choice_index": question.correct_choice_index,
                    }
                    for index, question in enumerate(quiz.questions, start=1)
                ]
            },
        )


__all__ = ["ReadingQuizExtension"]
