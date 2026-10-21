#!/usr/bin/env python3
"""Sinh các đoạn LaTeX (bảng) cho report.tex từ test-cases.xlsx.

Cách dùng:  python3 latex/gen_tables.py
Kết quả:     latex/gen_requirements.tex
             latex/gen_traceability.tex
             latex/gen_testcases.tex
             latex/gen_execution.tex
"""
import os
import re

import openpyxl

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(BASE, "test-cases.xlsx")
OUT = os.path.join(BASE, "latex")

ESC = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_\allowbreak{}",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


# Ký tự Unicode cần chuyển sang lệnh LaTeX
UNICODE = {
    "≤": r"$\leq$",
    "≥": r"$\geq$",
    "→": r"$\rightarrow$",
    "←": r"$\leftarrow$",
    "×": r"$\times$",
    "–": "--",
    "—": "---",
    "“": "``",
    "”": "''",
    "‘": "`",
    "’": "'",
    "•": r"$\bullet$",
    "…": r"\ldots{}",
}


def esc(text):
    """Chuyển chuỗi thường thành chuỗi LaTeX an toàn."""
    if text is None:
        return ""
    out = []
    for ch in str(text):
        if ch in UNICODE:
            out.append(UNICODE[ch])
        else:
            out.append(ESC.get(ch, ch))
    return "".join(out)


def cell(text, mode="p"):
    """Chuẩn bị nội dung một ô: xuống dòng -> \newline, chuẩn hóa khoảng trắng."""
    if text is None:
        text = ""
    text = str(text).replace("\r\n", "\n").replace("\r", "\n")
    parts = [p.strip() for p in text.split("\n")]
    parts = [p for p in parts if p != ""]
    if not parts:
        return ""
    if mode == "l":
        return r" \\ ".join(esc(p) for p in parts)
    return r" \newline ".join(esc(p) for p in parts)


def rows(ws, start=2):
    for r in ws.iter_rows(min_row=start, values_only=True):
        if all(v is None for v in r):
            continue
        yield r


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def gen_requirements(wb):
    ws = wb["Requirements"]
    body = []
    body.append(r"\small")
    body.append(r"\setlength{\tabcolsep}{4pt}")
    body.append(r"\begin{longtable}{|p{1.9cm}|p{5.6cm}|c|c|c|p{1.8cm}|}")
    body.append(r"\caption{Đặc tả yêu cầu chức năng và phi chức năng kèm đánh giá rủi ro}")
    body.append(r"\label{tab:requirements} \\")
    body.append(r"\hline")
    body.append(
        r"\textbf{Mã} & \textbf{Mô tả yêu cầu} & \textbf{P} & \textbf{I} & "
        r"\textbf{R} & \textbf{Mức rủi ro} \\")
    body.append(r"\hline")
    body.append(r"\endfirsthead")
    body.append(r"\hline")
    body.append(
        r"\textbf{Mã} & \textbf{Mô tả yêu cầu} & \textbf{P} & \textbf{I} & "
        r"\textbf{R} & \textbf{Mức rủi ro} \\")
    body.append(r"\hline")
    body.append(r"\endhead")
    body.append(r"\hline \endfoot")
    for r in rows(ws):
        code, desc, p, i, risk = r[0], r[1], r[2], r[3], r[4]
        level = "Cao" if risk >= 10 else ("Trung bình" if risk >= 6 else "Thấp")
        body.append(
            "{} & {} & {} & {} & {} & {} \\\\".format(
                esc(code), cell(desc), esc(p), esc(i), esc(risk), esc(level)))
        body.append(r"\hline")
    body.append(r"\end{longtable}")
    body.append(r"\normalsize")
    write("gen_requirements.tex", "\n".join(body) + "\n")


def gen_traceability(wb):
    ws = wb["Traceability"]
    body = []
    body.append(r"\small")
    body.append(r"\setlength{\tabcolsep}{4pt}")
    body.append(r"\begin{longtable}{|p{1.5cm}|p{1.5cm}|p{5.3cm}|p{1.2cm}|p{2.7cm}|}")
    body.append(r"\caption{Ma trận truy vết yêu cầu $\rightarrow$ kỹ thuật $\rightarrow$ test case}")
    body.append(r"\label{tab:traceability} \\")
    body.append(r"\hline")
    body.append(
        r"\textbf{Yêu cầu} & \textbf{Kỹ thuật} & \textbf{Test case} & "
        r"\textbf{Lỗi} & \textbf{Lớp test} \\")
    body.append(r"\hline")
    body.append(r"\endfirsthead")
    body.append(r"\hline")
    body.append(
        r"\textbf{Yêu cầu} & \textbf{Kỹ thuật} & \textbf{Test case} & "
        r"\textbf{Lỗi} & \textbf{Lớp test} \\")
    body.append(r"\hline")
    body.append(r"\endhead")
    body.append(r"\hline \endfoot")
    for r in rows(ws):
        req, tech, tcs, bug, layer = r[0], r[1], r[2], r[3], r[4]
        bug = "--" if not bug else bug
        body.append(
            "{} & {} & {} & {} & {} \\\\".format(
                esc(req), esc(tech), cell(tcs), esc(bug), esc(layer)))
        body.append(r"\hline")
    body.append(r"\end{longtable}")
    write("gen_traceability.tex", "\n".join(body) + "\n")


def gen_testcases(wb):
    ws = wb["TestCases"]
    body = []
    body.append(r"\small")
    body.append(r"\setlength{\tabcolsep}{3pt}")
    body.append(
        r"\begin{longtable}{|p{2.0cm}|p{1.4cm}|p{2.25cm}|p{2.05cm}|p{2.75cm}|p{3.2cm}|}")
    body.append(r"\caption{Bảng test case chi tiết của toàn nhóm (36 test case)}")
    body.append(r"\label{tab:all-tc} \\")
    body.append(r"\hline")
    body.append(
        r"\textbf{TC ID} & \textbf{Y/cầu} & \textbf{Tiền điều kiện} & "
        r"\textbf{Dữ liệu} & \textbf{Bước thực hiện} & \textbf{Kết quả mong đợi} \\")
    body.append(r"\hline")
    body.append(r"\endfirsthead")
    body.append(r"\hline")
    body.append(
        r"\textbf{TC ID} & \textbf{Y/cầu} & \textbf{Tiền điều kiện} & "
        r"\textbf{Dữ liệu} & \textbf{Bước thực hiện} & \textbf{Kết quả mong đợi} \\")
    body.append(r"\hline")
    body.append(r"\endhead")
    body.append(r"\hline \endfoot")
    for r in rows(ws):
        tc_id = str(r[0]).split(":")[0].strip()
        body.append(
            "\\textbf{{{}}} & {} & {} & {} & {} & {} \\\\".format(
                esc(tc_id), cell(r[1]), cell(r[2]), cell(r[3]), cell(r[4]),
                cell(r[5])))
        body.append(r"\hline")
    body.append(r"\end{longtable}")
    body.append(r"\normalsize")
    write("gen_testcases.tex", "\n".join(body) + "\n")


def gen_execution(wb):
    ws = wb["Execution"]
    body = []
    body.append(r"\small")
    body.append(r"\setlength{\tabcolsep}{3pt}")
    body.append(
        r"\begin{longtable}{|p{2.0cm}|p{2.7cm}|p{2.9cm}|p{4.9cm}|p{1.6cm}|}")
    body.append(r"\caption{Kết quả thực thi test case thủ công (NV4)}")
    body.append(r"\label{tab:execution} \\")
    body.append(r"\hline")
    body.append(
        r"\textbf{Mã TC} & \textbf{Ngày / Người thực hiện} & \textbf{Môi trường} & "
        r"\textbf{Kết quả thực tế} & \textbf{Trạng thái} \\")
    body.append(r"\hline")
    body.append(r"\endfirsthead")
    body.append(r"\hline")
    body.append(
        r"\textbf{Mã TC} & \textbf{Ngày / Người thực hiện} & \textbf{Môi trường} & "
        r"\textbf{Kết quả thực tế} & \textbf{Trạng thái} \\")
    body.append(r"\hline")
    body.append(r"\endhead")
    body.append(r"\hline \endfoot")
    for r in rows(ws):
        tc_id, who, env, actual, status = r[0], r[1], r[2], r[3], r[4]
        st = esc(status)
        if st and "Fail" in st:
            st = r"\textbf{" + st + "}"
        body.append(
            "{} & {} & {} & {} & {} \\\\".format(
                esc(tc_id), cell(who), cell(env), cell(actual), st))
        body.append(r"\hline")
    body.append(r"\end{longtable}")
    body.append(r"\normalsize")
    write("gen_execution.tex", "\n".join(body) + "\n")


def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    gen_requirements(wb)
    gen_traceability(wb)
    gen_testcases(wb)
    gen_execution(wb)


if __name__ == "__main__":
    main()
