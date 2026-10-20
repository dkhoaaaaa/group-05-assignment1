#!/usr/bin/env python3
"""Tạo file test-cases.xlsx cho assignment"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

def create_excel():
    wb = openpyxl.Workbook()
    
    # Định nghĩa styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
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
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    # ============ SHEET 1: Requirements ============
    ws = wb.active
    ws.title = "Requirements"
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
    ws = wb.create_sheet("Traceability")
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
    ws = wb.create_sheet("TestCases")
    headers = ["TC ID", "Test Objective", "Technique", "Pre-conditions", "Test Steps", "Test Data", "Expected Result", "FR/NFR"]
    style_header(ws, headers)
    
    test_cases = [
        # FR-04 Sort (8 EP + boundary)
        ["TC-SORT-EP1", "Kiểm tra sắp xếp Name A→Z", "EP", "Đã đăng nhập", "1. Mở dropdown sort\n2. Chọn 'Name (A to Z)'", "Sort option: az", "Danh sách sắp xếp theo tên từ A đến Z", "FR-04"],
        ["TC-SORT-EP2", "Kiểm tra sắp xếp Name Z→A", "EP", "Đã đăng nhập", "1. Mở dropdown sort\n2. Chọn 'Name (Z to A)'", "Sort option: za", "Danh sách sắp xếp theo tên từ Z đến A", "FR-04"],
        ["TC-SORT-EP3", "Kiểm tra sắp xếp Price low→high", "EP", "Đã đăng nhập", "1. Mở dropdown sort\n2. Chọn 'Price (low to high)'", "Sort option: lohi", "Danh sách sắp xếp theo giá tăng dần", "FR-04"],
        ["TC-SORT-EP4", "Kiểm tra sắp xếp Price high→low", "EP", "Đã đăng nhập", "1. Mở dropdown sort\n2. Chọn 'Price (high to low)'", "Sort option: hilo", "Danh sách sắp xếp theo giá giảm dần", "FR-04"],
        ["TC-SORT-EP5", "Kiểm tra không chọn sort (default)", "EP", "Đã đăng nhập", "1. Không thay đổi sort", "Default", "Thứ tự mặc định ban đầu", "FR-04"],
        ["TC-SORT-BVA1", "Kiểm tra sắp xếp với giá thấp nhất (boundary)", "BVA", "Đã đăng nhập", "1. Thêm sản phẩm giá thấp nhất\n2. Sort low→high\n3. Kiểm tra vị trí", "Sản phẩm giá min", "Sản phẩm giá thấp nhất ở vị trí đầu tiên", "FR-04"],
        ["TC-SORT-BVA2", "Kiểm tra sắp xếp với giá cao nhất (boundary)", "BVA", "Đã đăng nhập", "1. Thêm sản phẩm giá cao nhất\n2. Sort high→low\n3. Kiểm tra vị trí", "Sản phẩm giá max", "Sản phẩm giá cao nhất ở vị trí đầu tiên", "FR-04"],
        ["TC-SORT-BVA3", "Kiểm tra sắp xếp với sản phẩm giữa (boundary)", "BVA", "Đã đăng nhập", "1. Sort Name A→Z\n2. Kiểm tra sản phẩm giữa danh sách", "Sản phẩm mid", "Sản phẩm giữa đúng vị trí", "FR-04"],
        # NFR-01 Performance
        ["TC-NFR-01", "Đo thời gian load trang inventory", "Performance", "Đăng nhập với performance_glitch_user", "1. Đăng nhập với user 'performance_glitch_user'\n2. Đo thời gian từ click login đến khi trang load xong\n3. Lặp 5 lần\n4. Tính trung vị", "Username: performance_glitch_user\nPassword: secret_sauce", "Trung vị thời gian load ≤ 3 giây", "NFR-01"],
    ]
    
    for row_idx, row_data in enumerate(test_cases, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='top', wrap_text=True)
    
    auto_width(ws)
    ws.row_dimensions[1].height = 20
    
    # ============ SHEET 4: Execution ============
    ws = wb.create_sheet("Execution")
    headers = ["TC ID", "Test Date", "Tester", "Result (PASS/FAIL)", "Actual Result", "Notes"]
    style_header(ws, headers)
    
    executions = [
        ["TC-SORT-EP1", "", "Hùng", "", "", ""],
        ["TC-SORT-EP2", "", "Hùng", "", "", ""],
        ["TC-SORT-EP3", "", "Hùng", "", "", ""],
        ["TC-SORT-EP4", "", "Hùng", "", "", ""],
        ["TC-SORT-EP5", "", "Hùng", "", "", ""],
        ["TC-SORT-BVA1", "", "Hùng", "", "", ""],
        ["TC-SORT-BVA2", "", "Hùng", "", "", ""],
        ["TC-SORT-BVA3", "", "Hùng", "", "", ""],
        ["TC-NFR-01", "", "Hùng", "", "", ""],
    ]
    
    for row_idx, row_data in enumerate(executions, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(vertical='center')
    
    auto_width(ws)
    
    # ============ SHEET 5: Bugs ============
    ws = wb.create_sheet("Bugs")
    headers = ["Bug ID", "TC ID", "Summary", "Severity", "Status", "Evidence Path", "Notes"]
    style_header(ws, headers)
    
    bugs = [
        ["BUG-01", "TC-NFR-01", "Trang inventory load chậm hơn 3 giây với performance_glitch_user", "Medium", "Open", "evidence/TC-NFR-01.png", "Trung vị 5 lần đo ~5 giây, vượt ngưỡng 3 giây"],
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
    print(f"Đã tạo file: {output_path}")

if __name__ == "__main__":
    create_excel()
