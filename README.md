🥷 Danh sách kỹ năng / hành động trong game

1. Tấn công cơ bản (Light Attacks / Combo)
	•	Light1 / Light2 / Light3
	•	Tấn công nhanh, sát thương nhỏ → trung bình.
	•	Có thể chain combo: Light1 → Light2 → Light3.
	•	Mỗi chiêu có damage, stun, knockback, cooldown riêng.
	•	Khi trúng mục tiêu sẽ hồi lại SP (sp_gain_on_hit).
	•	Riêng Char B (Sát Thủ) khi kết thúc combo (light3) còn được bonus SP (sp_gain_on_combo_finish).

2. Đòn trên không (Air Attack)
	•	Air attack
	•	Thực hiện khi nhân vật đang ở trên không.
	•	Có giới hạn số lần (mỗi lần nhảy chỉ dùng được vài lần → air_attacks_left).
	•	Gây sát thương và stun, thường để chặn đối phương khi nhảy hoặc áp sát.

3. Đòn đặc biệt (Special Attack)
	•	SP Skill (mất SP để dùng, tốn SP_COST_SPECIAL).
	•	Char A (Kiếm Sĩ Lửa)
	•	Gây sát thương lớn, knockback mạnh.
	•	Có hitbox rộng (hitbox_size), thích hợp để kết thúc combo hoặc dồn damage.
	•	Char B (Sát Thủ Tốc Độ)
	•	Đòn đánh đa hit (3 lần), đánh theo frame quy định (hit_frames).
	•	Có range box (kiểm tra phạm vi trước khi lao đến).
	•	Nếu trúng mục tiêu → combo đa hit, nếu hụt thì dịch chuyển nhanh đến vị trí ngẫu nhiên trong range.
	•	Rất phù hợp để mở combo hoặc bắt bài khi đối thủ thủ thế.

4. Phòng thủ (Defend)
	•	Khi giữ defend:
	•	Giảm sát thương nhận vào (defense_modifier).
	•	Khi block thành công, được hồi SP (sp_gain_on_block).
	•	Không di chuyển / không tấn công được trong lúc phòng thủ.

5. Roll (Lướt né)
	•	Roll thường (Normal Roll)
	•	Tốn SP (SP_COST_ROLL).
	•	Có i-frame (invincible frame) từ ROLL_IFRAME_START đến ROLL_IFRAME_DURATION → giúp né chiêu.
	•	Có cooldown (ROLL_COOLDOWN_DURATION).
	•	Có thể roll trên đất và cả trên không (giới hạn số lần: air_rolls_left).
	•	Tech Roll (Roll khi bị đánh)
	•	Nếu vừa trúng đòn → có cửa sổ 150ms (TECH_ROLL_WINDOW) để phản ứng.
	•	Tốn nhiều SP hơn (SP_COST_TECH_ROLL).
	•	Khi thành công: thoát stun, bật trạng thái xuyên thấu (tech_rolling) → không bị pushbox cản.
	•	Hữu ích để thoát khỏi combo hoặc corner trap.

6. Jump (Nhảy)
	•	Nhảy tối đa jumps_left = 2 (double jump).
	•	Khi nhảy, tốc độ ngang thay đổi thành air_speed.
	•	Reset số lần nhảy khi chạm đất.

7. Passive SP Gain (Hồi SP thụ động)
	•	Mỗi PASSIVE_SP_GAIN_RATE ms → hồi lại PASSIVE_SP_GAIN_AMOUNT.
	•	Đảm bảo dù không đánh vẫn có thể tích SP để dùng skill đặc biệt / roll.

8. Knockback & Hit Stun
	•	Khi trúng đòn:
	•	Nhân vật bị trừ HP theo damage (giảm nếu defend).
	•	Bị đẩy lùi (knockback).
	•	Bị stun (không thể điều khiển) trong thời gian stun_duration.
	•	Trong trạng thái stun có thể Tech Roll nếu kịp input.

⸻

📊 So sánh nhanh giữa 2 nhân vật

🔥 Char A – Kiếm Sĩ Lửa
	•	HP cao (110), SP 100.
	•	Đòn đặc biệt sát thương to, diện rộng.
	•	Combo đơn giản nhưng damage ổn định.
	•	Roll/defend tiêu chuẩn.

🥷 Char B – Sát Thủ Tốc Độ
	•	HP thấp (90), SP 100.
	•	Combo nhanh, nhiều hit.
	•	Đòn đặc biệt đánh nhiều lần, có dịch chuyển.
	•	Thưởng SP khi kết thúc combo.
	•	Cơ động hơn, dễ snowball nhưng rủi ro cao.

⸻

👉 Tổng kết:
	•	Light/Combo → tạo nhịp độ và hồi SP.
	•	Air Attack → kiểm soát không trung.
	•	Special → chiêu kết liễu / mở combo mạnh, tốn SP.
	•	Defend → giảm damage, hồi SP khi block.
	•	Roll/Tech Roll → cơ chế phòng thủ nâng cao, né chiêu hoặc thoát combo.
	•	Passive SP → giữ game cân bằng, luôn có thể hồi SP dần dần.

⸻
AIR ATTACK ĐÁNH TỐI ĐA TRÊN KHÔNG 2 LẦN, CÓ THỂ SỬ DỤNG SPECIAL ATTACK
MỖI 5s sau nếu đủ sp thì sẽ sử dụng đc lại chiêu đặc biệt
NẾU BẤM VÀO D - PHÒNG THỦ THÌ SẼ DÃ Ở THẾ THỦ KO PHẢI LÀ ĂN HIT
NẾU ĐANG BỊ ĐÁNH ÁP SÁT CÓ THỂ BẤM SPACE LƯỚT QUA ĐỐI THỦ TUY TỐN NHIỀU MANA HƠN