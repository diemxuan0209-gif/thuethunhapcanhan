import streamlit as st

# Cấu hình trang web của ứng dụng
st.set_page_config(page_title="App Tính Thuế TNCN Việt Nam 2026", page_icon="💰", layout="centered")

# --- CHÈN LOGO THEO FILE TRỰC TIẾP ---
st.image("logo.jpg")

# --- THÔNG TIN THÀNH VIÊN VÀ ĐỀ TÀI ---
st.markdown("### 📝 **Đề Tài 7_Nguyễn Trần Diễm Xuân**")

st.title("💰 Ứng Dụng Tính Thuế Thu Nhập Cá Nhân")
st.write("Cập nhật đầy đủ Lương, Thưởng, Tăng ca, Phụ cấp theo luật thuế mới nhất năm 2026")

st.markdown("---")

# --- PHẦN NHẬP DỮ LIỆU ĐẦU VÀO (TIẾNG VIỆT) ---
st.subheader("📋 Nhập thông tin thu nhập tháng này của bạn")

gross_salary = st.number_input(
    "1. Lương chính / Lương Gross (VND):", 
    min_value=0, value=30000000, step=500000, format="%d"
)

bonus_pay = st.number_input(
    "2. Tiền thưởng / Bonus (VND):", 
    min_value=0, value=0, step=500000, format="%d"
)

overtime_pay = st.number_input(
    "3. Tiền lương tăng ca / làm thêm giờ (VND):", 
    min_value=0, value=0, step=500000, format="%d"
)

st.markdown("**4. Các khoản phụ cấp nhận bằng tiền mặt:**")
col_sub1, col_sub2 = st.columns(2)
with col_sub1:
    lunch_allowance = st.number_input("Phụ cấp ăn trưa (VND):", min_value=0, value=730000, step=50000)
with col_sub2:
    other_allowance = st.number_input("Phụ cấp điện thoại, xăng xe (VND):", min_value=0, value=500000, step=50000)

dependents = st.number_input(
    "5. Số người phụ thuộc bạn đang nuôi dưỡng (người):", 
    min_value=0, value=1, step=1
)

st.markdown("---")

# --- PHẦN NÚT BẤM KÍCH HOẠT TÍNH TOÁN ---
if st.button("🧮 Tính Thuế & Nhận Kết Quả", type="primary"):
    
    # 1. Tính tổng thu nhập thực tế
    total_income = gross_salary + bonus_pay + overtime_pay + lunch_allowance + other_allowance
    
    # 2. Bảo hiểm bắt buộc (10.5%)
    bhxh = gross_salary * 0.08
    bhyt = gross_salary * 0.015
    bhtn = gross_salary * 0.01
    total_insurance = bhxh + bhyt + bhtn
    
    # 3. Giảm trừ gia cảnh luật mới 2026
    self_reduction = 15500000  
    dependent_reduction = dependents * 6200000  
    total_reduction = self_reduction + dependent_reduction
    
    # 4. Thu nhập được miễn thuế
    exempt_lunch = min(lunch_allowance, 730000)
    exempt_allowance = other_allowance 
    total_exempt_income = overtime_pay + exempt_lunch + exempt_allowance
    
    # 5. Tính thu nhập tính thuế cuối cùng
    assessable_income = max(0, total_income - total_exempt_income - total_insurance - total_reduction)
    
    # 6. Thuật toán bảng lũy tiến 5 bậc năm 2026
    tax = 0
    brackets = [
        {"limit": 10000000, "rate": 0.05, "desc": "Bậc 1: Đến 10 triệu đồng (5%)"},
        {"limit": 30000000, "rate": 0.10, "desc": "Bậc 2: Trên 10 đến 30 triệu đồng (10%)"},
        {"limit": 60000000, "rate": 0.20, "desc": "Bậc 3: Trên 30 đến 60 triệu đồng (20%)"},
        {"limit": 100000000, "rate": 0.30, "desc": "Bậc 4: Trên 60 đến 100 triệu đồng (30%)"},
        {"limit": float('inf'), "rate": 0.35, "desc": "Bậc 5: Trên 100 triệu đồng (35%)"}
    ]
    
    temp_income = assessable_income
