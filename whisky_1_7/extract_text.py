#!/usr/bin/env python3
"""Raw text extractor for whisky smart parser. Dumps all text from any file."""
import sys, os

def extract(path):
    ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
    if ext == "xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        lines = []
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                for cell in row:
                    if cell is not None:
                        v = str(cell).strip()
                        if v:
                            lines.append(v)
        return "
".join(lines)
    elif ext == "docx":
        import zipfile, re
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.DOTALL)
        lines = []
        for p in paras:
            text = re.sub(r"<[^>]+>", " ", p)
            text = " ".join(text.split())
            if text:
                lines.append(text)
        return "
".join(lines)
    else:
        with open(path, "r", errors="replace") as f:
            return f.read()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: extract_text.py <file>")
    # materialize from rclone VFS
    import shutil, tempfile
    src = sys.argv[1]
    tmp = src + "._extract_tmp"
    try:
        shutil.copy2(src, tmp)
        print(extract(tmp))
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
