# Whisky v1.8 — User Guide

## What it does

Drop a file on Google Drive with the right prefix, get shell command results back as CSV.
The server reads your file, extracts commands via AI, runs them, and writes results.

## Supported formats

- **Google Sheets (.xlsx)** — one command per cell in column A
- **Google Docs (.docx)** — one command per paragraph
- **Plain text (.txt)** — one command per line
- **CSV (.csv)** — one command per row

## How to send a task

1. Create your file (Sheets or Docs) with shell commands, one per cell/paragraph
2. Name it: 
   Example: 
3. Drop it in the root of the shared Google Drive folder
4. Wait ~5 seconds — results appear in 

## Writing commands

**Google Sheets — wrap in bash -c for paths and arguments:**

    bash -c "df -h && uptime"
    bash -c "cp /tmp/file.txt /home/whisky/dest/"

**Google Docs — use single-quoted echo for writing files:**

    echo 'int main() { return 0; }' > hello.c
    gcc hello.c -o hello && ./hello

Avoid double-quoted strings with backslash-n (
) inside literals —
the connector pipeline does not preserve escape sequences reliably.
Verify file writes with  before compiling or running.

## Reading results

Results are in :

| Column | Content |
|--------|---------|
| Command | The shell command that ran |
| Output | stdout + stderr from that command |

If a command fails, the error is captured in the Output column — the task continues.
