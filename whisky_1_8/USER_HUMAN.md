# Whisky v1.8 — User Guide

## What it does

Drop a file on Google Drive with the right prefix.
Whisky sends it to Claude, extracts shell commands, runs them on the server,
and puts results back into Drive as a CSV.

## Supported formats

Google Sheets (.xlsx), CSV (.csv), Google Docs (.docx), plain text (.txt).

## File naming convention

    PREFIX + DATE + DESCRIPTION + .ext

- PREFIX identifies the target server and version (assigned by your operator)
- DATE is optional but recommended: YYYYMMDD
- DESCRIPTION is a short label with underscores, no spaces
- ext: .xlsx, .csv, .docx, or .txt

Example: WSC1_1_8_20260506_disk_audit.docx

The full filename without extension becomes the task name used in output paths.

## How to send a task

1. Create your file in the Drive root (not in a subfolder).
2. For Sheets: commands in column A, one per row, no header.
3. For Docs: one command per paragraph.
4. Name it following the convention above and save.
5. Wait a few seconds — the input file disappears when picked up.

## Output structure on Drive

    WHISKY_OUT/
    └── WSC1_1_8_20260506_disk_audit/
        ├── WSC1_1_8_20260506_disk_audit.docx    copy of input
        ├── WSC1_1_8_20260506_disk_audit.csv     results
        └── result/                               files created during task

Open the CSV in Sheets. Two columns: Command and Output.
If a command fails, the error appears in Output and execution continues.

## Command examples

Google Sheets (column A):

    df -h
    uptime
    bash -c "ls -la /home/whisky && free -m"

Google Docs (one paragraph each):

    echo 'int main() { return 0; }' > hello.c
    gcc hello.c -o hello && ./hello

## Tips

- In Sheets: wrap commands with paths in bash -c to avoid CSV quoting issues.
- In Docs: use single-quoted echo for writing file contents.
- File must be in the Drive root, not in a subfolder.
- Re-running the same task name overwrites previous output.
