#!/usr/bin/env python3
"""Cập nhật file test-cases.xlsx với kết quả thực tế sau khi chạy test"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from datetime import date

def update_excel():
    wb = openpyxl.load_workbook("/home/hung/Desktop/ktpm/group-XX-assignment1/test-cases.xlsx")

    # Styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    pass_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")  # xanh
    fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")  # đỏ
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    def style_header(ws, headers):
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = thin_border

    def auto_width(ws):
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = min(max_length + 2, 60)
            ws.column_dimensions[column_letter].width = adjusted_width

    # ============ SHEET 1: Requirements ============
    ws = wb["Requirements"]
    headers = ["Requirement ID", "Description", "Type", "Priority", "Owner"]
    style_header(ws, headers)

    requirements = [
        ["FR-01", "Đăng nhập - Username phân biệt hoa/thường, bắt lỗi đúng", "FR", "High", "TV1"],
        ["FR-02", "Giỏ hàng - Thêm/xóa sản phẩm, Badge 1-6, ẩn khi rỗng", "FR", "High", "TV2"],
        ["FR-03", "Thanh toán - Form bắt buộc, Tax 8%, Total chính xác", "FR", "High", "TV3/TV4"],
        ["FR-04", "Sắp xếp - 4 chiều: Name A-Z, Z-A, Price low-high, high-low", "FR", "Medium", "TV5"],
        ["NFR-01", "Hiệu năng - Thời gian load inventory ≤ 3 giây (trung vị 5 lần)", "NFR", "Medium", "TV5"],
    ]

    for row_idx, row_data in enumerate(requirements, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='center')

    auto_width(ws)

    # ============ SHEET 2: Traceability ============
    ws = wb["Traceability"]
    headers = ["Test Case ID", "Requirement ID", "Traceability Status"]
    style_header(ws, headers)

    traceability = [
        ["TC-SORT-EP1", "FR-04", "Direct"],
        ["TC-SORT-EP2", "FR-04", "Direct"],
        ["TC-SORT-EP3", "FR-04", "Direct"],
        ["TC-SORT-EP4", "FR-04", "Direct"],
        ["TC-SORT-EP5", "FR-04", "Direct"],
        ["TC-SORT-BVA1", "FR-04", "Direct"],
        ["TC-SORT-BVA2", "FR-04", "Direct"],
        ["TC-SORT-BVA3", "FR-04", "Direct"],
        ["TC-NFR-01", "NFR-01", "Direct"],
    ]

    for row_idx, row_data in enumerate(traceability, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='center')

    auto_width(ws)

    # ============ SHEET 3: TestCases ============
    ws = wb["TestCases"]
    headers = ["TC ID", "Test Objective", "Technique", "Pre-conditions", "Test Steps", "Test Data", "Expected Result", "FR/NFR"]
    style_header(ws, headers)

    test_cases = [
        ["TC-SORT-EP1", "Kiểm tra sắp xếp Name A→Z", "EP", "Đã đăng nhập", "1. Mở dropdown sort\n2. Chọn 'Name (A to Z)'", "Sort option: az", "Danh sách sắp xếp theo tên từ A đến Z", "FR-04"],
        ["TC-SORT-EP2", "Kiểm tra sắp xếp Name Z→A", "EP", "Đã đăng nhập", "1. Mở dropdown sort\n2. Chọn 'Name (Z to A)'", "Sort option: za", "Danh sách sắp xếp theo tên từ Z đến A", "FR-04"],
        ["TC-SORT-EP3", "Kiểm tra sắp xếp Price low→high", "EP", "Đã đăng nhập", "1. Mở dropdown sort\n2. Chọn 'Price (low to high)'", "Sort option: lohi", "Danh sách sắp xếp theo giá tăng dần", "FR-04"],
        ["TC-SORT-EP4", "Kiểm tra sắp xếp Price high→low", "EP", "Đã đăng nhập", "1. Mở dropdown sort\n2. Chọn 'Price (high to low)'", "Sort option: hilo", "Danh sách sắp xếp theo giá giảm dần", "FR-04"],
        ["TC-SORT-EP5", "Kiểm tra không chọn sort (default)", "EP", "Đã đăng nhập", "1. Không thay đổi sort", "Default", "Thứ tự mặc định ban đầu", "FR-04"],
        ["TC-SORT-BVA1", "Kiểm tra sắp xếp với giá thấp nhất (boundary)", "BVA", "Đã đăng nhập", "1. Sort low→high\n2. Kiểm tra sản phẩm đầu tiên có giá thấp nhất", "6 sản phẩm", "Sản phẩm giá thấp nhất ($7.99) ở vị trí đầu tiên", "FR-04"],
        ["TC-SORT-BVA2", "Kiểm tra sắp xếp với giá cao nhất (boundary)", "BVA", "Đã đăng nhập", "1. Sort high→low\n2. Kiểm tra sản phẩm đầu tiên có giá cao nhất", "6 sản phẩm", "Sản phẩm giá cao nhất ($49.99) ở vị trí đầu tiên", "FR-04"],
        ["TC-SORT-BVA3", "Kiểm tra sắp xếp với sản phẩm giữa (boundary)", "BVA", "Đã đăng nhập", "1. Sort Name A→Z\n2. Kiểm tra sản phẩm giữa danh sách", "6 sản phẩm", "Sản phẩm giữa thỏa mãn thứ tự alphabet", "FR-04"],
        ["TC-NFR-01", "Đo thời gian load trang inventory (performance_glitch_user)", "Performance", "Đăng nhập với performance_glitch_user", "1. Login với 'performance_glitch_user'\n2. Mở trang inventory\n3. Đo thời gian load\n4. Lặp 5 lần, tính trung vị", "Username: performance_glitch_user\nPassword: secret_sauce\n5 lần đo", "Trung vị thời gian load ≤ 3 giây", "NFR-01"],
    ]

    for row_idx, row_data in enumerate(test_cases, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)

    auto_width(ws)
    ws.row_dimensions[1].height = 20

    # ============ SHEET 4: Execution (ĐÃ ĐIỀN KẾT QUẢ) ============
    ws = wb["Execution"]
    headers = ["TC ID", "Test Date", "Tester", "Result (PASS/FAIL)", "Actual Result", "Notes"]
    style_header(ws, headers)

    # Kết quả thực tế sau khi chạy automation
    executions = [
        # TC-ID, Test Date, Tester, Result, Actual Result, Notes
        ["TC-SORT-EP1", date.today().strftime("%Y-%m-%d"), "Hùng", "PASS",
         "6 sản phẩm sắp xếp đúng A→Z theo tên",
         "Danh sách thực tế khớp với Collections.sort()"],
        ["TC-SORT-EP2", date.today().strftime("%Y-%m-%d"), "Hùng", "PASS",
         "6 sản phẩm sắp xếp đúng Z→A theo tên",
         "Danh sách thực tế khớp với reverseOrder()"],
        ["TC-SORT-EP3", date.today().strftime("%Y-%m-%d"), "Hùng", "PASS",
         "6 sản phẩm sắp xếp đúng low→high theo giá",
         "Sử dụng @ValueSource và @MethodSource parameterized test"],
        ["TC-SORT-EP4", date.today().strftime("%Y-%m-%d"), "Hùng", "PASS",
         "6 sản phẩm sắp xếp đúng high→low theo giá",
         "Tất cả 4 sort options hoạt động đúng"],
        ["TC-SORT-EP5", date.today().strftime("%Y-%m-%d"), "Hùng", "PASS",
         "Default sort = A→Z (thứ tự mặc định của app)",
         "Default không chọn sort = thứ tự A→Z"],
        ["TC-SORT-BVA1", date.today().strftime("%Y-%m-%d"), "Hùng", "PASS",
         "Sản phẩm đầu tiên sau sort lohi có giá $7.99 (min)",
         "Boundary: giá thấp nhất đúng ở vị trí index 0"],
        ["TC-SORT-BVA2", date.today().strftime("%Y-%m-%d"), "Hùng", "PASS",
         "Sản phẩm đầu tiên sau sort hilo có giá $49.99 (max)",
         "Boundary: giá cao nhất đúng ở vị trí index 0"],
        ["TC-SORT-BVA3", date.today().strftime("%Y-%m-%d"), "Hùng", "PASS",
         "Sản phẩm giữa (index 2/3) thỏa mãn prev <= middle <= next",
         "Boundary: sản phẩm giữa đúng vị trí trong danh sách đã sort"],
        ["TC-NFR-01", date.today().strftime("%Y-%m-%d"), "Hùng", "FAIL",
         "Trung vị 5 lần đo = 5.228s (vượt ngưỡng 3s). Chi tiết: [5.246, 5.274, 5.206, 5.211, 5.228]",
         "BUG-01: performance_glitch_user gây chậm ~5.2s. Baseline standard_user chỉ 0.201s"],
    ]

    for row_idx, row_data in enumerate(executions, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='center', wrap_text=True)
            # Tô màu kết quả
            if col_idx == 4:
                if value == "PASS":
                    cell.fill = pass_fill
                elif value == "FAIL":
                    cell.fill = fail_fill

    auto_width(ws)

    # ============ SHEET 5: Bugs (cập nhật chi tiết) ============
    ws = wb["Bugs"]
    headers = ["Bug ID", "TC ID", "Summary", "Severity", "Status", "Evidence Path", "Notes"]
    style_header(ws, headers)

    bugs = [
        ["BUG-01", "TC-NFR-01", "Trang inventory load chậm hơn 3 giây với performance_glitch_user", "Medium", "Open",
         "evidence/TC-NFR-01.png",
         "Trung vị 5 lần đo = 5.228s, vượt ngưỡng 3s. Các lần đo: [5.246s, 5.274s, 5.206s, 5.211s, 5.228s]. "
         + "Baseline standard_user chỉ 0.201s → Bug do performance_glitch_user cố tình gây chậm."],
    ]

    for row_idx, row_data in enumerate(bugs, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='center', wrap_text=True)

    auto_width(ws)

    # Lưu file
    output_path = "/home/hung/Desktop/ktpm/group-XX-assignment1/test-cases.xlsx"
    wb.save(output_path)
    print(f"Đã cập nhật file: {output_path}")
    print(f"  - Execution: 8 PASS, 1 FAIL (BUG-01)")
    print(f"  - TC-NFR-01: Trung vị = 5.228s (ngưỡng 3s)")

if __name__ == "__main__":
    update_excel()
