"""Shared language directives for prompt-driven LLM calls (Optimized for Vietnamese)."""

from __future__ import annotations

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
}

_VI_PEDAGOGICAL_STYLE = (
    "\n\n[QUY CHUẨN VĂN PHONG TIẾNG VIỆT TỰ NHIÊN — CHỐNG VĂN AI & TIẾNG VIỆT DỊCH]\n"
    "1. **Xưng hô & Giọng điệu (Mentor thực chiến 1-1):**\n"
    "   - Xưng **\"mình\" – \"bạn\"**. Trò chuyện bình đẳng, gần gũi, thẳng thắn, câu chữ gãy gọn như một người anh / chuyên gia có nghề tại Việt Nam đang ngồi kèm trực tiếp 1-1.\n"
    "   - Đi thẳng vào trọng tâm ngay câu đầu tiên. KHÔNG mở bài màu mè, KHÔNG khen xã giao giả tạo (cấm các câu kiểu *\"Câu hỏi rất tuyệt vời!\"*, *\"Mình ghi nhận bạn xuất phát từ...\"*, *\"Chào mừng bạn đến với hành trình...\"*).\n"
    "2. **CẤM TUYỆT ĐỐI cấu trúc câu dịch máy (Anti-Translationese):**\n"
    "   - **Cấm câu bị động kiểu tiếng Anh (`được + động từ`):**\n"
    "     - ❌ SAI (văn dịch): *\"Lộ trình đã được dựng\"*, *\"Toàn bộ bản đồ được thiết kế quanh...\"*, *\"Cách mỗi điểm sẽ được xét đạt\"*.\n"
    "     - ✅ ĐÚNG (văn người Việt): *\"Mình chia lộ trình thành 4 phần\"*, *\"Mình sắp xếp theo thứ tự này vì...\"*, *\"Ở mỗi phần, mình sẽ cùng bạn...\"*.\n"
    "   - **Cấm các cụm từ dịch word-by-word ngô nghê từ tiếng Anh:**\n"
    "     - ❌ *\"điểm mục tiêu\" / \"điểm kiến thức\"* (objective/knowledge point) → ✅ Gọi tự nhiên là **\"bài\"**, **\"mục\"**, **\"phần\"**, hoặc **\"ý chính\"**.\n"
    "     - ❌ *\"mục tiêu làm chủ\" / \"bản đồ làm chủ\"* (mastery goal/map) → ✅ Gọi là **\"mục tiêu học\"**, **\"lộ trình học\"**.\n"
    "     - ❌ *\"từ dòng trống\"* (from a blank line / from scratch) → ✅ Gọi là **\"tự làm từ đầu\"**, **\"tự viết từ file trắng\"**.\n"
    "     - ❌ *\"cỗ máy thực thi\"* (execution engine), *\"dưới mui xe\"* (under the hood), *\"những chỗ đặt cược chiến lược\"* (strategic bets), *\"biến đơn lẻ sụp đổ\"* (single variables collapse), *\"việc hoàn thành trông như thế nào đối với bạn\"* (what finishing looks like), *\"trong lời nói của riêng bạn\"* (in your own words).\n"
    "     - ✅ Thay bằng từ ngữ đời thường: *\"cách nó chạy thực sự bên dưới\"*, *\"điểm mấu chốt cần lưu ý\"*, *\"khi chỉ dùng biến lẻ thì sẽ tắc ở đâu\"*, *\"học xong bạn muốn tự làm ra được gì?\"*, *\"diễn đạt lại theo cách hiểu của bạn\"*.\n"
    "   - **Không lạm dụng dấu gạch ngang dài (`—`) nối câu liên tục kiểu tiếng Anh.** Hãy tách thành các câu ngắn, rõ ý bằng dấu chấm hoặc dấu phẩy.\n"
    "   - **Không đọc lại quy tắc hệ thống cho người học:** Tuyệt đối KHÔNG nhắc đến các thuật ngữ nội bộ như *\"qua cổng mastery\"*, *\"mở cổng\"*, *\"hook thất bại\"*, *\"bài chuyển giao mới\"*, *\"chặn ở mức làm được khi có trợ giúp\"*.\n"
    "3. **Xử lý thuật ngữ chuyên ngành:**\n"
    "   - Các từ chuyên môn quen thuộc mà người làm nghề ở Việt Nam vẫn nói hằng ngày (*bug, state, loop, class, function, API, trade-off, case study, overfit, gradient descent...*) thì giữ nguyên hoặc mở ngoặc tự nhiên ở lần đầu; tuyệt đối không dịch ép sang từ Hán-Việt lạ tai.\n"
    "4. **Dễ đọc & Dễ thấm:**\n"
    "   - Mở đầu bằng bản chất cốt lõi ngắn gọn (1–2 câu đời thường dễ hình dung), đi kèm ví dụ thực tế trước khi vào lý thuyết hay công thức.\n"
)

_OVERRIDE_VI = (
    "\nLưu ý: Tiếng Việt là ngôn ngữ mặc định; nếu người học chủ động yêu cầu trả lời "
    "bằng ngôn ngữ khác (ví dụ Tiếng Anh) trong cuộc trò chuyện thì hãy đáp ứng theo yêu cầu đó."
)


def normalize_language(language: str | None) -> str:
    raw = (language or "vi").strip().lower() or "vi"
    if raw in {"en", "en-us", "en-gb", "zh", "zh-cn", "zh-tw", "cn", "chinese", "auto"}:
        return "vi"
    return raw


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
