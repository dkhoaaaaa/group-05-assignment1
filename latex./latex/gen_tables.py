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


TC_ID = re.compile(r"TC-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*(?:\.[0-9]+)?(?:--[0-9]+\.[0-9]+)?")


def nobreak_ids(latex):
    """Bọc mã test case (TC-...) trong \\mbox để không bị ngắt giữa mã."""
    return TC_ID.sub(lambda m: r"\mbox{" + m.group(0) + "}", latex)


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
        return nobreak_ids(r" \\ ".join(esc(p) for p in parts))
    return nobreak_ids(r" \newline ".join(esc(p) for p in parts))


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


def longtable(caption, label, colspec, header, body_rows, size=r"\small",
              tabcolsep="4pt"):
    """Dựng một longtable có header tô nền, lặp lại ở mỗi trang."""
    hdr = " & ".join(r"\textbf{" + h + "}" for h in header)
    out = [
        r"{" + size,
        r"\setlength{\tabcolsep}{" + tabcolsep + "}",
        r"\renewcommand{\arraystretch}{1.25}",
        r"\arrayrulecolor{black!55}",
        r"\begin{longtable}{" + colspec + "}",
        r"\caption{" + caption + r"}",
        r"\label{" + label + r"} \\",
        r"\hline",
        r"\rowcolor{tablehead} " + hdr + r" \\",
        r"\hline",
        r"\endfirsthead",
        r"\multicolumn{" + str(len(header)) + r"}{@{}l}{\small\itshape "
        r"(tiếp bảng ở trang trước)} \\",
        r"\hline",
        r"\rowcolor{tablehead} " + hdr + r" \\",
        r"\hline",
        r"\endhead",
        r"\hline",
        r"\endfoot",
        r"\hline",
        r"\endlastfoot",
    ]
    for row in body_rows:
        out.append(row + r" \\")
        out.append(r"\hline")
    out.append(r"\end{longtable}")
    out.append(r"}")
    return "\n".join(out) + "\n"


def gen_requirements(wb):
    ws = wb["Requirements"]
    body = []
    for r in rows(ws):
        code, desc, p, i, risk = r[0], r[1], r[2], r[3], r[4]
        level = "Cao" if risk >= 10 else ("Trung bình" if risk >= 6 else "Thấp")
        body.append(" & ".join([
            esc(code), cell(desc), esc(p), esc(i), esc(risk), esc(level)]))
    write("gen_requirements.tex", longtable(
        "Đặc tả yêu cầu chức năng và phi chức năng kèm đánh giá rủi ro",
        "tab:requirements",
        r"|L{1.7cm}|L{8.0cm}|C{0.8cm}|C{0.8cm}|C{0.8cm}|L{2.3cm}|",
        ["Mã", "Mô tả yêu cầu", "P", "I", "R", "Mức rủi ro"], body))


def gen_traceability(wb):
    ws = wb["Traceability"]
    body = []
    for r in rows(ws):
        req, tech, tcs, bug, layer = r[0], r[1], r[2], r[3], r[4]
        bug = "--" if not bug else bug
        body.append(" & ".join([
            esc(req), esc(tech), cell(tcs), esc(bug), esc(layer)]))
    write("gen_traceability.tex", longtable(
        r"Ma trận truy vết yêu cầu $\rightarrow$ kỹ thuật $\rightarrow$ test case",
        "tab:traceability",
        r"|L{1.8cm}|L{2.2cm}|L{5.3cm}|L{1.4cm}|L{3.8cm}|",
        ["Yêu cầu", "Kỹ thuật", "Test case", "Lỗi", "Lớp test"], body))


def gen_testcases(wb):
    """Bảng 6 cột, rất rộng -> đặt trong trang A4 nằm ngang."""
    ws = wb["TestCases"]
    body = []
    for r in rows(ws):
        tc_id = str(r[0]).split(":")[0].strip()
        body.append(" & ".join([
            r"\textbf{" + nobreak_ids(esc(tc_id)) + "}",
            cell(r[1]), cell(r[2]), cell(r[3]), cell(r[4]), cell(r[5])]))
    table = longtable(
        "Bảng test case chi tiết của toàn nhóm (36 test case)",
        "tab:all-tc",
        r"|L{3.5cm}|L{1.9cm}|L{4.6cm}|L{3.7cm}|L{5.1cm}|L{5.1cm}|",
        ["TC ID", "Y/cầu", "Tiền điều kiện", "Dữ liệu", "Bước thực hiện",
         "Kết quả mong đợi"], body, size=r"\footnotesize", tabcolsep="3pt")
    write("gen_testcases.tex",
          "\\clearpage\n"
          "\\newgeometry{width=25.7cm, height=16.6cm, left=2.0cm, top=2.2cm, "
          "headheight=14.5pt, headsep=0.6cm, footskip=0.9cm}\n"
          "\\paperwidth=29.7cm \\paperheight=21cm\n"
          "\\pdfpagewidth=\\paperwidth \\pdfpageheight=\\paperheight\n"
          + table + "\\clearpage\n\\restoregeometry\n"
          "\\paperwidth=21cm \\paperheight=29.7cm\n"
          "\\pdfpagewidth=\\paperwidth \\pdfpageheight=\\paperheight\n")


def gen_execution(wb):
    ws = wb["Execution"]
    body = []
    for r in rows(ws):
        tc_id, who, env, actual, status = r[0], r[1], r[2], r[3], r[4]
        st = esc(status)
        if st and "Fail" in st:
            st = r"\textcolor{failred}{\textbf{" + st + "}}"
        elif st and "Pass" in st:
            st = r"\textcolor{passgreen}{" + st + "}"
        body.append(" & ".join([
            nobreak_ids(esc(tc_id)), cell(who), cell(env), cell(actual), st]))
    write("gen_execution.tex", longtable(
        "Kết quả thực thi test case thủ công (NV4)",
        "tab:execution",
        r"|L{3.4cm}|L{2.6cm}|L{2.6cm}|L{4.7cm}|L{1.4cm}|",
        ["Mã TC", "Ngày / Người thực hiện", "Môi trường", "Kết quả thực tế",
         "Trạng thái"], body))


def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    gen_requirements(wb)
    gen_traceability(wb)
    gen_testcases(wb)
    gen_execution(wb)


if __name__ == "__main__":
    main()
