import type { MasteryMode } from "@/lib/mastery-mode";

export const QUICK_MODE_TEMPLATES = [
  {
    id: "zero-to-one",
    badge: "🎯 Học từ con số 0",
    title: "Học một mảng mới từ đầu, nắm nhanh phần cốt lõi",
    emblem: "🧠",
    template:
      "Mình muốn học [Tên chủ đề, VD: Lập trình Python / Kinh tế vĩ mô / Machine Learning] từ đầu. Mình muốn hiểu rõ bản chất từng phần chứ không học vẹt, học xong có thể tự áp dụng vào việc thực tế.",
  },
  {
    id: "project-first",
    badge: "🛠️ Học để làm dự án",
    title: "Đang cần làm một dự án hoặc giải quyết việc cụ thể",
    emblem: "🧭",
    template:
      "Mình đang cần làm [Mô tả dự án hoặc công việc của bạn]. Nhờ bạn lọc ra những phần kiến thức cần thiết nhất để mình vừa học vừa bắt tay vào làm luôn.",
  },
  {
    id: "doc-grounded",
    badge: "📚 Học theo tài liệu",
    title: "Đọc hiểu sâu & áp dụng sách / tài liệu đính kèm",
    emblem: "🔭",
    template:
      "Mình muốn học kỹ tài liệu đính kèm về [Chủ đề]. Nhờ bạn dẫn dắt từng phần trọng tâm, giải thích những chỗ khó hiểu bằng ví dụ thực tế và ra bài tập để mình tự kiểm tra lại.",
  },
] as const;

export const INKGEST_MODE_PRESENTATION: Record<
  MasteryMode,
  {
    noteKey: string;
    emptyTitleKey: string;
    emptyBodyKey: string;
  }
> = {
  outline: {
    noteKey:
      "Đang ở bước lên khung lộ trình học. Khi đã ưng ý với lộ trình, bạn bấm 'Bắt đầu học ngay' để vào bài đầu tiên nhé.",
    emptyTitleKey: "Lên khung lộ trình học",
    emptyBodyKey:
      "Mình sẽ dựa trên mục tiêu (và tài liệu nếu có) để lọc ra những phần cốt lõi nhất, sắp xếp theo trình tự dễ hiểu từ gốc đến ngọn.",
  },
  study: {
    noteKey: "",
    emptyTitleKey: "",
    emptyBodyKey:
      "Đi từ bài toán thực tế, hiểu rõ bản chất bên dưới, sau đó tự tay giải quyết các tình huống và bài tập vận dụng.",
  },
  review: {
    noteKey:
      "Chế độ Ôn tập — kiểm tra lại các phần đã học qua tình huống thực tế mới để nhớ lâu hơn.",
    emptyTitleKey: "Ôn lại các phần đã học",
    emptyBodyKey:
      "Thử sức lại với các bài đến hạn ôn tập bằng những câu hỏi vận dụng mới.",
  },
};

export const INKGEST_STARTER_KEYS: Record<MasteryMode, readonly [string, string, string]> = {
  outline: [
    "Lên giúp mình lộ trình học gọn, đi thẳng vào những phần cốt lõi nhất",
    "Hỏi nhanh mình vài câu về nền tảng hiện tại để chỉnh lộ trình cho vừa sức",
    "Lộ trình ổn rồi, mình bắt đầu học bài đầu tiên luôn nhé",
  ],
  study: [
    "Ra thử 1 câu bài tập xem phần này mình đã nắm được chưa",
    "Giải thích phần này từ bài toán thực tế cho dễ hình dung",
    "Cho mình một bài tập vận dụng thực tế để tự làm thử",
  ],
  review: [
    "Ôn lại các bài đến hạn hôm nay qua tình huống thực tế mới",
    "Kiểm tra lại những chỗ hôm trước mình hay nhầm",
    "Ra một bài tổng hợp kết hợp các phần mình đã học",
  ],
};

export const INKGEST_OUTLINE_OPENING_MESSAGE =
  "Mình muốn học chủ đề này. Bạn xem qua mục tiêu của mình rồi lên giúp mình một lộ trình học tinh gọn, tập trung vào những phần cốt lõi quan trọng nhất nhé.";

export const INKGEST_DASHBOARD_COPY = {
  subtitle:
    "Học sâu bản chất, nắm chắc phần cốt lõi và rèn kỹ năng thực tế cho mọi lĩnh vực.",
  createButtonLabel: "Tạo lộ trình học mới",
  emptyTitle: "Bạn muốn học gì hôm nay?",
  emptyDescription:
    "Bấm nút bên dưới để bắt đầu một chủ đề mới từ con số 0, học để làm dự án thực tế, hoặc học kèm với sách/tài liệu của bạn.",
} as const;
