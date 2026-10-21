#!/usr/bin/env python3
"""
Recreate test-cases.xlsx to match the format of test-cases123.xlsx
Group style: plain cells (no fill, no border), wrap_text=True, Calibri 11pt
Headers in Vietnamese, P/I/R for risk, 5-col Traceability with blank-row separators.
"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

OUTPUT = "/home/hung/Desktop/ktpm/group-XX-assignment1/test-cases.xlsx"

# Style helpers
FONT = "Calibri"
SZ = 11
BOLD_FONT = Font(name=FONT, size=SZ, bold=True)
PLAIN_FONT = Font(name=FONT, size=SZ, bold=False)
BLUE_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
WHITE_BOLD = Font(name=FONT, size=SZ, bold=True, color="FFFFFF")
THIN_BORDER = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin")
)

def plain_cell(ws, row, col, value):
    c = ws.cell(row=row, column=col, value=value)
    c.font = PLAIN_FONT
    c.alignment = Alignment(horizontal="general", vertical="bottom", wrap_text=True)
    return c

def blue_header_cell(ws, row, col, value):
    c = ws.cell(row=row, column=col, value=value)
    c.font = WHITE_BOLD
    c.fill = BLUE_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=False)
    c.border = THIN_BORDER
    return c

def auto_col_width(ws, min_w=8, max_w=60):
    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
            except Exception:
                pass
        ws.column_dimensions[col_letter].width = max(min(max_len + 2, max_w), min_w)

# ============================================================
# Build workbook
# ============================================================
wb = openpyxl.Workbook()
wb.remove(wb.active)  # remove default sheet

# ============================================================
# SHEET 1: Requirements
# Columns: Mã Yêu Cầu | Mô tả yêu cầu | Xác suất lỗi (P) | Mức tác động (I) | Rủi ro (R = P x I)
# ============================================================
ws = wb.create_sheet("Requirements")
# Column widths (matching group file)
ws.column_dimensions["A"].width = 16
ws.column_dimensions["B"].width = 60
ws.column_dimensions["C"].width = 6
ws.column_dimensions["D"].width = 10
ws.column_dimensions["E"].width = 9

# Header row
for col, hdr in enumerate([
    "Mã Yêu Cầu", "Mô tả yêu cầu",
    "Xác suất lỗi (P)", "Mức tác động (I)", "Rủi ro (R = P x I)"
], 1):
    plain_cell(ws, 1, col, hdr)

# Data rows
reqs = [
    # FR-04 decomposed into 4 sub-requirements (one per sort criterion)
    ("FR-04.1", "Hệ thống cho phép sắp xếp danh sách sản phẩm theo tên từ A đến Z (Name A→Z).", 2, 4, 8),
    ("FR-04.2", "Hệ thống cho phép sắp xếp danh sách sản phẩm theo tên từ Z đến A (Name Z→A).", 2, 4, 8),
    ("FR-04.3", "Hệ thống cho phép sắp xếp danh sách sản phẩm theo giá tăng dần (Price low→high).", 2, 4, 8),
    ("FR-04.4", "Hệ thống cho phép sắp xếp danh sách sản phẩm theo giá giảm dần (Price high→low).", 2, 4, 8),
    # Blank separator
    None,
    # NFR-01
    ("NFR-01", "Thời gian load trang inventory phải ≤ 3 giây (trung vị của 5 lần đo) với tài khoản standard_user.", 1, 5, 5),
]
for i, row_data in enumerate(reqs, 2):
    if row_data is None:
        # blank separator row — leave empty
        continue
    plain_cell(ws, i, 1, row_data[0])  # Mã
    plain_cell(ws, i, 2, row_data[1])  # Mô tả
    plain_cell(ws, i, 3, str(row_data[2]))  # P
    plain_cell(ws, i, 4, str(row_data[3]))  # I
    plain_cell(ws, i, 5, str(row_data[4]))  # R

auto_col_width(ws)

# ============================================================
# SHEET 2: Traceability
# Columns: Yêu cầu | Kỹ thuật | Test case | Lỗi | Lớp test
# ============================================================
ws = wb.create_sheet("Traceability")
ws.column_dimensions["A"].width = 14
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 60
ws.column_dimensions["D"].width = 10
ws.column_dimensions["E"].width = 24

# Header
for col, hdr in enumerate(["Yêu cầu", "Kỹ thuật", "Test case", "Lỗi", "Lớp test"], 1):
    plain_cell(ws, 1, col, hdr)

trace_rows = [
    # FR-04 rows
    ("FR-04.1", "EP", "TC-SORT-EP1, TC-SORT-EP2", "", "SortTest.java"),
    ("FR-04.2", "EP", "TC-SORT-EP3, TC-SORT-EP4", "", "SortTest.java"),
    ("FR-04.3", "EP, BVA", "TC-SORT-BVA1, TC-SORT-BVA2, TC-SORT-BVA3", "", "SortTest.java"),
    ("FR-04.4", "BVA", "TC-SORT-BVA1, TC-SORT-BVA2", "", "SortTest.java"),
    # Blank separator
    None,
    # NFR-01 row
    ("NFR-01", "Performance", "TC-NFR-01", "BUG-01", "PerformanceTest.java"),
]
for i, row_data in enumerate(trace_rows, 2):
    if row_data is None:
        continue
    plain_cell(ws, i, 1, row_data[0])
    plain_cell(ws, i, 2, row_data[1])
    plain_cell(ws, i, 3, row_data[2])
    plain_cell(ws, i, 4, row_data[3])
    plain_cell(ws, i, 5, row_data[4])

auto_col_width(ws)

# ============================================================
# SHEET 3: TestCases
# Columns: Mã TC / Tên | Yêu cầu / Kỹ thuật | Tiền điều kiện
#          | Dữ liệu | Bước thực hiện | Kết quả mong đợi
#          | Expected Result | FR/NFR
# G1/H1 = blue header + border (matching group file)
# A-F data rows: plain (no border, matching group file)
# G-H data rows: bordered (matching group file)
# ============================================================
ws = wb.create_sheet("TestCases")
ws.column_dimensions["A"].width = 14
ws.column_dimensions["B"].width = 60
ws.column_dimensions["C"].width = 13
ws.column_dimensions["D"].width = 39
ws.column_dimensions["E"].width = 60
ws.column_dimensions["F"].width = 50
ws.column_dimensions["G"].width = 20
ws.column_dimensions["H"].width = 8

# Header row (A-F = plain, G-H = blue header + border)
for col, hdr in enumerate([
    "Mã TC / Tên", "Yêu cầu / Kỹ thuật", "Tiền điều kiện",
    "Dữ liệu", "Bước thực hiện", "Kết quả mong đợi",
    "Expected Result", "FR/NFR"
], 1):
    if col <= 6:
        plain_cell(ws, 1, col, hdr)
    else:
        blue_header_cell(ws, 1, col, hdr)

# Data
tc_rows = [
    # TC ID | Yêu cầu/Kỹ thuật | Tiền điều kiện | Dữ liệu | Bước thực hiện | Kết quả mong đợi | Expected Result | FR/NFR
    ("TC-SORT-EP1",
     "FR-04.1 / EP",
     "Đã đăng nhập standard_user; đang ở trang inventory",
     "Sort option: az",
     "1. Mở dropdown sort\n2. Chọn 'Name (A to Z)'",
     "Danh sách sắp xếp theo tên từ A đến Z",
     "Danh sách sắp xếp theo tên từ A đến Z",
     "FR-04"),

    ("TC-SORT-EP2",
     "FR-04.2 / EP",
     "Đã đăng nhập standard_user; đang ở trang inventory",
     "Sort option: za",
     "1. Mở dropdown sort\n2. Chọn 'Name (Z to A)'",
     "Danh sách sắp xếp theo tên từ Z đến A",
     "Danh sách sắp xếp theo tên từ Z đến A",
     "FR-04"),

    ("TC-SORT-EP3",
     "FR-04.3 / EP",
     "Đã đăng nhập standard_user; đang ở trang inventory",
     "Sort option: lohi",
     "1. Mở dropdown sort\n2. Chọn 'Price (low to high)'",
     "Danh sách sắp xếp theo giá tăng dần",
     "Danh sách sắp xếp theo giá tăng dần",
     "FR-04"),

    ("TC-SORT-EP4",
     "FR-04.4 / EP",
     "Đã đăng nhập standard_user; đang ở trang inventory",
     "Sort option: hilo",
     "1. Mở dropdown sort\n2. Chọn 'Price (high to low)'",
     "Danh sách sắp xếp theo giá giảm dần",
     "Danh sách sắp xếp theo giá giảm dần",
     "FR-04"),

    ("TC-SORT-EP5",
     "FR-04 / EP",
     "Đã đăng nhập standard_user; đang ở trang inventory",
     "Default (không chọn sort)",
     "1. Không thay đổi sort",
     "Thứ tự mặc định ban đầu của app",
     "Thứ tự mặc định ban đầu",
     "FR-04"),

    ("TC-SORT-BVA1",
     "FR-04.3 / BVA",
     "Đã đăng nhập standard_user; đang ở trang inventory với đủ 6 sản phẩm",
     "6 sản phẩm",
     "1. Chọn sort 'Price (low to high)'\n2. Kiểm tra sản phẩm đầu tiên",
     "Sản phẩm giá thấp nhất ($7.99) ở vị trí đầu tiên",
     "Sản phẩm giá thấp nhất ($7.99) ở vị trí đầu tiên",
     "FR-04"),

    ("TC-SORT-BVA2",
     "FR-04.4 / BVA",
     "Đã đăng nhập standard_user; đang ở trang inventory với đủ 6 sản phẩm",
     "6 sản phẩm",
     "1. Chọn sort 'Price (high to low)'\n2. Kiểm tra sản phẩm đầu tiên",
     "Sản phẩm giá cao nhất ($49.99) ở vị trí đầu tiên",
     "Sản phẩm giá cao nhất ($49.99) ở vị trí đầu tiên",
     "FR-04"),

    ("TC-SORT-BVA3",
     "FR-04.1 / BVA",
     "Đã đăng nhập standard_user; đang ở trang inventory với đủ 6 sản phẩm",
     "6 sản phẩm",
     "1. Chọn sort 'Name (A to Z)'\n2. Kiểm tra sản phẩm giữa danh sách",
     "Sản phẩm giữa thỏa mãn thứ tự alphabet (prev <= middle <= next)",
     "Sản phẩm giữa thỏa mãn thứ tự alphabet",
     "FR-04"),

    ("TC-NFR-01",
     "NFR-01 / Performance",
     "Đăng nhập với performance_glitch_user; đang ở trang login",
     "Username: performance_glitch_user\nPassword: secret_sauce",
     "1. Đăng nhập với 'performance_glitch_user'\n2. Đo thời gian từ click Login đến khi trang inventory load xong\n3. Lặp 5 lần\n4. Tính trung vị",
     "Trung vị thời gian load ≤ 3 giây",
     "Trung vị thời gian load ≤ 3 giây",
     "NFR-01"),
]

for i, row_data in enumerate(tc_rows, 2):
    # A-F: plain
    for col in range(1, 7):
        plain_cell(ws, i, col, row_data[col - 1])
    # G: bordered, plain font
    gc = ws.cell(row=i, column=7, value=row_data[6])
    gc.font = PLAIN_FONT
    gc.alignment = Alignment(horizontal="general", vertical="top", wrap_text=True)
    gc.border = THIN_BORDER
    # H: bordered, plain font
    hc = ws.cell(row=i, column=8, value=row_data[7])
    hc.font = PLAIN_FONT
    hc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    hc.border = THIN_BORDER

auto_col_width(ws)

# ============================================================
# SHEET 4: Execution
# Columns: Mã TC | Ngày / Người | Môi trường | Kết quả thực tế | Trạng thái
# ============================================================
ws = wb.create_sheet("Execution")
ws.column_dimensions["A"].width = 14
ws.column_dimensions["B"].width = 20
ws.column_dimensions["C"].width = 40
ws.column_dimensions["D"].width = 60
ws.column_dimensions["E"].width = 12

# Header
for col, hdr in enumerate([
    "Mã TC", "Ngày / Người", "Môi trường", "Kết quả thực tế", "Trạng thái"
], 1):
    plain_cell(ws, 1, col, hdr)

# Data
executions = [
    # TC ID | Ngày/Người | Môi trường | Kết quả thực tế | Trạng thái
    ("TC-SORT-EP1", "20/10/2026 - Hùng", "Chrome, standard_user",
     "6 sản phẩm sắp xếp đúng A→Z theo tên. Danh sách thực tế khớp với Collections.sort().", "Pass"),
    ("TC-SORT-EP2", "20/10/2026 - Hùng", "Chrome, standard_user",
     "6 sản phẩm sắp xếp đúng Z→A theo tên. Danh sách thực tế khớp với reverseOrder().", "Pass"),
    ("TC-SORT-EP3", "20/10/2026 - Hùng", "Chrome, standard_user",
     "6 sản phẩm sắp xếp đúng low→high theo giá. Sử dụng @ValueSource và @MethodSource.", "Pass"),
    ("TC-SORT-EP4", "20/10/2026 - Hùng", "Chrome, standard_user",
     "6 sản phẩm sắp xếp đúng high→low theo giá. Tất cả 4 sort options hoạt động đúng.", "Pass"),
    ("TC-SORT-EP5", "20/10/2026 - Hùng", "Chrome, standard_user",
     "Default sort = A→Z (thứ tự mặc định của app, không chọn sort).", "Pass"),
    ("TC-SORT-BVA1", "20/10/2026 - Hùng", "Chrome, standard_user",
     "Sản phẩm đầu tiên sau sort lohi có giá $7.99 (min). Boundary giá thấp nhất đúng ở index 0.", "Pass"),
    ("TC-SORT-BVA2", "20/10/2026 - Hùng", "Chrome, standard_user",
     "Sản phẩm đầu tiên sau sort hilo có giá $49.99 (max). Boundary giá cao nhất đúng ở index 0.", "Pass"),
    ("TC-SORT-BVA3", "20/10/2026 - Hùng", "Chrome, standard_user",
     "Sản phẩm giữa (index 2/3) thỏa mãn prev <= middle <= next. Boundary sản phẩm giữa đúng vị trí.", "Pass"),
    ("TC-NFR-01", "20/10/2026 - Hùng", "Chrome, performance_glitch_user",
     "Trung vị 5 lần đo = 5.228s (vượt ngưỡng 3s). Chi tiết: [5.246, 5.274, 5.206, 5.211, 5.228]. Baseline standard_user chỉ 0.201s.", "Fail"),
]

for i, row_data in enumerate(executions, 2):
    for col, val in enumerate(row_data, 1):
        plain_cell(ws, i, col, val)

auto_col_width(ws)

# ============================================================
# SHEET 5: Bugs
# Columns: Mã / Tiêu đề | Mức nghiêm trọng | Môi trường
#          | Tiền điều kiện | Bước tái hiện | Kết quả mong đợi
#          | Kết quả thực tế | Bằng chứng
# ============================================================
ws = wb.create_sheet("Bugs")
ws.column_dimensions["A"].width = 8
ws.column_dimensions["B"].width = 11
ws.column_dimensions["C"].width = 60
ws.column_dimensions["D"].width = 10
ws.column_dimensions["E"].width = 8
ws.column_dimensions["F"].width = 24
ws.column_dimensions["G"].width = 60
ws.column_dimensions["H"].width = 24

# Header
for col, hdr in enumerate([
    "Mã / Tiêu đề", "Mức nghiêm trọng", "Môi trường",
    "Tiền điều kiện", "Bước tái hiện",
    "Kết quả mong đợi", "Kết quả thực tế", "Bằng chứng"
], 1):
    plain_cell(ws, 1, col, hdr)

# Bug data
bugs = [
    ("BUG-01: Trang inventory load chậm hơn 3 giây với performance_glitch_user",
     "Medium",
     "Chrome, 20/10/2026",
     "Đăng nhập bằng performance_glitch_user / secret_sauce",
     "1. Đăng nhập với performance_glitch_user\n2. Đo thời gian load trang inventory\n3. Lặp 5 lần, tính trung vị",
     "Trung vị thời gian load ≤ 3 giây",
     "Trung vị 5 lần đo = 5.228s, vượt ngưỡng 3s. Các lần đo: [5.246s, 5.274s, 5.206s, 5.211s, 5.228s]. Baseline standard_user chỉ 0.201s.",
     "evidence/TC-NFR-01.png"),
]

for i, row_data in enumerate(bugs, 2):
    for col, val in enumerate(row_data, 1):
        plain_cell(ws, i, col, val)

auto_col_width(ws)

# ============================================================
# Save
# ============================================================
wb.save(OUTPUT)
print(f"Đã tạo: {OUTPUT}")
