#!/usr/bin/env python3
"""
Wrapper giữ lại entry point cũ.

File test-cases.xlsx hiện được sinh bởi rebuild_test_cases.py theo đúng
format nhóm (test-cases123.xlsx): header tiếng Việt, cột P/I/R cho
Requirements, Traceability 5 cột, Execution 5 cột, Bugs 8 cột.

Script này chỉ gọi lại script mới để không bao giờ ghi đè file bằng
format cũ (tiếng Anh, 3 cột Traceability, 6 cột Execution).
"""

import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rebuild_test_cases.py")

if __name__ == "__main__":
    print("Đang sinh lại test-cases.xlsx theo format nhóm (rebuild_test_cases.py)...")
    subprocess.run([sys.executable, SCRIPT], check=True)
