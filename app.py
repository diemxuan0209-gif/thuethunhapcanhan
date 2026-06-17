import streamlit as st

# Cấu hình trang web của ứng dụng
st.set_page_config(page_title="App Tính Thuế TNCN Việt Nam 2026", page_icon="💰", layout="centered")

# --- CHÈN LOGO THEO FILE TRỰC TIẾP ---
# Hệ thống sẽ tìm file tên là logo.jpg nằm cùng thư mục với file app.py trên GitHub của bạn
st.image("logo.jpg")

# --- THÔNG TIN THÀNH VIÊN VÀ ĐỀ TÀI ---
st.markdown("### 📝 **Trường ĐẠI HỌC TÀI CHÍNH MARKETING_Đề Tài 7_Nguyễn Trần Diễm Xuân**")

st.title("💰 Ứng Dụng Tính Thuế Thu Nhập Cá Nhân")
st.write("Cập nhật đầy đủ Lương, Thưởng, Tăng ca, Phụ cấp theo luật thuế mới nhất năm 2026")

st.markdown("---")

# --- PHẦN NHẬP DỮ LIỆU ĐẦU VÀO (TIẾNG VIỆT) ---
st.subheader("📋 Nhập thông tin thu nhập tháng này của bạn")

# 1. Nhập mức lương chính
gross_salary = st.number_input(
    "1. Lương chính / Lương Gross (VND):", 
    min_value=0, value=30000000, step=500000, format="%d",
    help="Mức lương căn cứ để đóng bảo hiểm bắt buộc."
)

# 2. Nhập tiền thưởng
bonus_pay = st.number_input(
    "2. Tiền thưởng / Bonus (VND):", 
    min_value=0, value=0, step=500000, format="%d",
    help="Tiền thưởng hiệu suất, thưởng doanh số, thưởng lễ tết... (Khoản này tính thuế 100%)."
)

# 3. Nhập tiền tăng ca
overtime_pay = st.number_input(
    "3. Tiền lương tăng ca / làm thêm giờ (VND):", 
    min_value=0, value=0, step=500000, format="%d",
    help="Khoản tiền nhận được do làm thêm giờ (được miễn thuế TNCN)."
)

# 4. Các khoản phụ cấp phổ biến tại công ty
st.markdown("**4. Các khoản phụ cấp nhận bằng tiền mặt:**")
col_sub1, col_sub2 = st.columns(2)
with col_sub1:
    lunch_allowance = st.number_input("Phụ cấp ăn trưa (VND):", min_value=0, value=730000, step=50000)
with col_sub2:
    other_allowance = st.number_input("Phụ cấp điện thoại, xăng xe (VND):", min_value=0, value=500000, step=50000)

# 5. Nhập số người phụ thuộc
dependents = st.number_input(
    "5. Số người phụ thuộc bạn đang nuôi dưỡng (người):", 
    min_value=0, value=1, step=1
)

st.markdown("---")

# --- PHẦN LOGIC TÍNH TOÁN ---
if st.button("🧮 Tính Thuế & Nhận Kết Quả", type="primary"):
    
    # Tổng thu nhập thực tế nhận từ công ty
    total_income = gross_salary + bonus_pay + overtime_pay + lunch_allowance + other_allowance
    
    # 1. Bảo hiểm bắt buộc (Tính trên Lương chính - 10.5%)
    bhxh = gross_salary * 0.08
    bhyt = gross_salary * 0.015
    bhtn = gross_salary * 0.01
    total_insurance = bhxh + bhyt + bhtn
    
    # 2. Giảm trừ gia cảnh luật 2026
    self_reduction = 15500000  
    dependent_reduction = dependents * 6200000  
    total_reduction = self_reduction + dependent_reduction
    
    # 3. Xử lý các khoản thu nhập được MIỄN THUẾ
    exempt_lunch = min(lunch_allowance, 730000)
    exempt_allowance = other_allowance 
    total_exempt_income = overtime_pay + exempt_lunch + exempt_allowance
    
    # 4. Tính thu nhập tính thuế
    assessable_income = max(0, total_income - total_exempt_income - total_insurance - total_reduction)
    
    # 5. Tính toán thuế lũy tiến 5 bậc năm 2026
    tax = 0
    brackets = [
        {"limit": 10000000, "rate": 0.05, "desc": "Bậc 1: Đến 10 triệu đồng (5%)"},
        {"limit": 30000000, "rate": 0.10, "desc": "Bậc 2: Trên 10 đến 30 triệu đồng (10%)"},
        {"limit": 60000000, "rate": 0.20, "desc": "Bậc 3: Trên 30 đến 60 triệu đồng (20%)"},
        {"limit": 100000000, "rate": 0.30, "desc": "Bậc 4: Trên 60 đến 100 triệu đồng (30%)"},
        {"limit": float('inf'), "rate": 0.35, "desc": "Bậc 5: Trên 100 triệu đồng (35%)"}
    ]
    
    temp_income = assessable_income
    previous_limit = 0
    tax_breakdown = []
    
    for b in brackets:
        range_size = b["limit"] - previous_limit
        if temp_income > 0:
            taxable_in_bracket = min(temp_income, range_size)
            tax_in_bracket = taxable_in_bracket * b["rate"]
            tax += tax_in_bracket
            
            tax_breakdown.append({
                "Bậc thuế": b["desc"],
                "Thu nhập tính thuế ở bậc này": f"{taxable_in_bracket:,.0f} VND",
                "Tiền thuế phải nộp": f"{tax_in_bracket:,.0f} VND"
            })
            
            temp_income -= taxable_in_bracket
            previous_limit = b["limit"]
        else:
            break

    # 6. Lương NET thực nhận cuối cùng mang về nhà
    net_salary = total_income - total_insurance - tax

    # --- PHẦN HIỂN TH
