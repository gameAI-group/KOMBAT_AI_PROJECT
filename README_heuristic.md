Phân Tích & So Sánh: AI Heuristic vs. AI Rule-Based
Tài liệu này phân tích sự khác biệt cơ bản giữa hai mô hình AI được phát triển cho game: AI-RuleBased (dựa trên quy tắc) và AI-Heuristic (dựa trên kinh nghiệm và khả năng học hỏi).

1. AI Rule-Based (Nền Tảng)
   Đây là mô hình AI cơ bản, hoạt động như một cỗ máy phản ứng. Mọi quyết định của nó đều dựa trên một tập hợp các quy tắc "Nếu... thì..." cố định.
   Triết lý cốt lõi:
   Phản ứng tức thời: AI chỉ nhìn vào trạng thái hiện tại của trận đấu (khoảng cách, hành động của người chơi) và đưa ra quyết định ngay lập tức.
   Không có bộ nhớ: Nó không có khả năng ghi nhớ những gì đã xảy ra ở các lượt trước. Mỗi khoảnh khắc đều là một tình huống hoàn toàn mới.
   Dễ đoán: Vì hoạt động theo quy tắc cứng, một người chơi tinh ý có thể nhanh chóng tìm ra "công thức" để đánh bại nó.
   Logic hành vi:
   Nếu người chơi trong tầm đánh -> Tấn công.
   Nếu người chơi đang tấn công và ở gần -> Phòng thủ hoặc Lướt né (theo một tỷ lệ ngẫu nhiên).
   Nếu người chơi ở xa -> Áp sát.
