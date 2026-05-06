# Whisky v1.7 — User Guide

## What it does

Drop a Google Sheet with shell commands into your Drive root.
Whisky picks it up, runs the commands on the server, and puts results back.

## File naming convention

    PREFIX + DATE + DESCRIPTION + .xlsx

- **PREFIX** identifies the target server and version (assigned by your operator)
- **DATE** is optional but recommended: YYYYMMDD
- **DESCRIPTION** is a short label with underscores, no spaces

Example: WSC1_1_7_20260506_disk_audit.xlsx

The full filename without extension becomes the task name used in output paths.

## How to send a task

1. Open Google Sheets, create a new spreadsheet in the Drive root (not in a subfolder).
2. Enter shell commands in column A, one per row, starting at A1. No header row.
3. Name the file following the convention above and save.
4. Wait a few seconds — the input file disappears when picked up.

## Output structure on Drive

Results appear under WHISKY_OUT in your Drive root:

    WHISKY_OUT/
    └── WSC1_1_7_20260506_disk_audit/
        ├── WSC1_1_7_20260506_disk_audit.xlsx    copy of input
        └── WSC1_1_7_20260506_disk_audit.csv     results

Open the CSV in Sheets. Two columns: Command and Output.
If a command fails, the error appears in Output and execution continues.

## Example commands (column A)

    df -h
    uptime
    ls -la /home/whisky

For commands with paths or arguments, wrap in bash -c to avoid CSV quoting issues:

    bash -c "cp /tmp/file.txt /home/whisky/"
    bash -c "df -h && uptime"

## Tips

- File must be in the Drive root, not in a subfolder.
- Re-running the same task name overwrites previous output.
- Avoid backslash-n in string arguments; use && for multi-step commands instead.
