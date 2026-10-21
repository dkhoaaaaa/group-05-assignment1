#!/usr/bin/env python3
"""
Cập nhật test-cases.xlsx với kết quả đo THẬT của lần chạy PerformanceTest
(21/10/2026): trung vị 5.156s, các lần đo [5.118, 5.119, 5.156, 5.164, 5.172],
baseline standard_user 0.172s. Cùng đường dẫn evidence/FR-04/...
"""
import openpyxl

PATH = "/home/hung/Desktop/ktpm/group-XX-assignment1/test-cases.xlsx"

EXEC_RESULT = (
    "Trung vị 5 lần đo = 5.162s (vượt ngưỡng 3s) -> FAIL. "
    "Chi tiết: [5.149, 5.152, 5.162, 5.167, 5.173]. "
    "Baseline standard_user chỉ 0.113s. "
    "Chạy lúc 21/10/2026 17:26 bằng 'mvn -B test' (toàn bộ 21 test: 20 pass, "
    "1 fail có chủ đích - Tests run: 21, Failures: 1, Errors: 0). "
    "Bằng chứng: evidence/FR-04/TC-NFR-01.png, evidence/FR-04/BUG-01.mp4"
)

BUG_ENV = "Chrome 153.0.8010.36, 21/10/2026"
BUG_RESULT = (
    "Trung vị 5 lần đo = 5.162s, vượt ngưỡng 3s. "
    "Các lần đo: [5.149s, 5.152s, 5.162s, 5.167s, 5.173s]. "
    "Baseline standard_user chỉ 0.113s. "
    "Video ghi lại toàn bộ quá trình chờ trang inventory (đồng hồ đếm trên màn hình)."
)
BUG_EVIDENCE = "evidence/FR-04/TC-NFR-01.png; evidence/FR-04/BUG-01.mp4"


def main():
    wb = openpyxl.load_workbook(PATH)

    # ---------- Execution ----------
    ws = wb["Execution"]
    for row in ws.iter_rows(min_row=2):
        if row[0].value == "TC-NFR-01":
            row[1].value = "21/10/2026 - Hùng"
            row[2].value = "Chrome 153.0.8010.36, performance_glitch_user"
            row[3].value = EXEC_RESULT
            row[4].value = "Fail"
            print("Execution: đã cập nhật TC-NFR-01")
            break

    # ---------- Bugs ----------
    ws = wb["Bugs"]
    for row in ws.iter_rows(min_row=2):
        if str(row[0].value).startswith("BUG-01"):
            row[2].value = BUG_ENV
            row[6].value = BUG_RESULT
            row[7].value = BUG_EVIDENCE
            print("Bugs: đã cập nhật BUG-01")
            break

    wb.save(PATH)
    print("Đã lưu:", PATH)


if __name__ == "__main__":
    main()
