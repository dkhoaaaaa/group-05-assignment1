#!/usr/bin/env python3
"""Cập nhật bản sao dulieuesst/test-cases.xlsx cho khớp với kết quả đo thật."""
import openpyxl

PATH = "/home/hung/Desktop/ktpm/group-XX-assignment1/dulieutesst/test-cases.xlsx"

ACTUAL = (
    "Trung vị 5 lần đo = 5.162s (vượt ngưỡng 3s). "
    "Chi tiết: [5.149, 5.152, 5.162, 5.167, 5.173]. "
    "Baseline standard_user chỉ 0.113s. "
    "Chạy 21/10/2026 17:26 bằng 'mvn -B test' (21 test: 20 pass, 1 fail có chủ đích)."
)
NOTES = (
    "BUG-01: performance_glitch_user gây chậm ~5.2s. "
    "Baseline standard_user 0.113s. "
    "Bằng chứng: evidence/FR-04/TC-NFR-01.png, evidence/FR-04/BUG-01.mp4, "
    "evidence/FR-04/TC-NFR-01-run.log"
)
EVIDENCE = "evidence/FR-04/TC-NFR-01.png; evidence/FR-04/BUG-01.mp4"

wb = openpyxl.load_workbook(PATH)

ws = wb["Execution"]
for row in ws.iter_rows(min_row=2):
    if row[0].value == "TC-NFR-01":
        row[1].value = "2026-10-21"
        row[3].value = "FAIL"
        row[4].value = ACTUAL
        row[5].value = NOTES
        print("Execution: cập nhật TC-NFR-01")

ws = wb["Bugs"]
for row in ws.iter_rows(min_row=2):
    if row[0].value == "BUG-01":
        row[5].value = EVIDENCE
        row[6].value = NOTES
        print("Bugs: cập nhật BUG-01")

wb.save(PATH)
print("Đã lưu:", PATH)
