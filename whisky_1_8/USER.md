# Whisky v1.8 — User Guide

## What it does

Drop any file on Google Drive with the right prefix.
Whisky sends it to Claude (Haiku), extracts shell commands, runs them on the server,
and puts results back into Drive as a CSV.

## Supported formats

- Google Sheets (.xlsx), CSV (.csv) — one command per cell/row in column A
- Google Docs (.docx) — one command per paragraph
- Plain text (.txt) — one command per line

## File naming convention

    <PREFIX><DATE>_<DESCRIPTION>.<ext>

- **PREFIX** — identifies the target server and version (e.g. )
- **DATE** — optional but recommended: 
- **DESCRIPTION** — short label, underscores only, no spaces
- **ext** — .xlsx, .csv, .docx, or .txt

Example: 

The full filename minus extension becomes the **task name** used in output paths.

## How to send a task

1. Create your file (Sheets or Docs) in the **Drive root** (not in a subfolder).
2. Enter commands — one per cell (Sheets) or one per paragraph (Docs).
3. Name it following the convention above and save.
4. Wait a few seconds — input file disappears when picked up.

## Reading results

Results appear in Drive under :

    WHISKY_OUT/
    └── WSC1_1_8_20260506_hello_tango/
        ├── WSC1_1_8_20260506_hello_tango.docx   ← copy of your input
        ├── WSC1_1_8_20260506_hello_tango.csv    ← results
        └── result/                               ← files written during execution

Open the CSV in Sheets. Two columns:

| Command | Output |
|---------|--------|
| echo hello | hello |
| hostname | arm1 |

## Command tips (Google Sheets)

Wrap paths and arguments in  to avoid CSV quoting issues:

    bash -c "cp /tmp/file /home/whisky/"
    bash -c "df -h && uptime"

## Command tips (Google Docs)

Use single-quoted  for writing file contents — avoids escape conflicts:

    echo 'int main() { return 0; }' > hello.c
    gcc hello.c -o hello && ./hello

Verify each file write with  before compiling or running.
