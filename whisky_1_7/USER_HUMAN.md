# Whisky v1.7 — User Guide

## What it does

Drop a Google Sheet or CSV with shell commands into your Drive root.
Whisky runs them on the server and returns results as a CSV file.

## How to send a task

1. Open Google Sheets and create a new spreadsheet in the **Drive root** (not in a subfolder).
2. Enter shell commands in **column A**, one per row, starting at A1. No header row.
3. Name the file with the prefix for your target server, e.g. .
4. Wait a few seconds — results appear in .

## Command tips

- Wrap commands with path arguments in  to avoid CSV quoting issues:
  
- Avoid double quotes inside cell values — CSV export may double them unexpectedly.
- For multi-step operations, chain with :
  

## Reading results

Results CSV has two columns: **Command** and **Output** (stdout + stderr).
If a command fails, the error is captured — the task continues to the next command.

## Notes

- Input file is deleted after successful processing.
- Re-running the same task name overwrites previous output.
- Use  files instead of Sheets if you need to include commas in commands.
