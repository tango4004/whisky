# Whisky Project

A lightweight Drive-connected task runner for ARM/AMD servers.
Drop a file on Google Drive — get shell command results back as CSV.

---

## v1.7 — Hardcoded bash runner

**Goal:** minimal, zero-dependency task execution. No AI model required on the server.

The watcher reads shell commands from Google Sheets (column A) or CSV files,
runs them on the server, and writes results back to Drive as a CSV.

**Use when:** you have a server with rclone-mounted Drive and want reliable,
predictable command execution without any API keys or external dependencies.

**Supports:** .xlsx, .csv

**Quick start:**

    cd whisky_1_7 && cp .env.example .env && python3 whisky_1_7.py

---

## v1.8 — Claude smart parser

**Goal:** accept any file format, extract commands via AI, execute on the server.

The watcher sends the file contents to Claude (Haiku) for command extraction,
then executes whatever commands Claude returns. No hardcoded format assumptions.

**Use when:** you have an Anthropic API key and want to drop Google Docs, plain text,
or any structured file and have the server figure out what to run.

**Supports:** .xlsx, .csv, .docx, .txt

**Requires:** ANTHROPIC_API_KEY in .env

**Quick start:**

    cd whisky_1_8 && cp .env.example .env
    # fill in ANTHROPIC_API_KEY and WHISKY_PREFIX
    python3 whisky_1_8.py

---

## Key differences

| | v1.7 | v1.8 |
|---|---|---|
| Command source | Spreadsheet cells (literal) | Claude (Haiku) extracts from any text |
| Formats | .xlsx, .csv | .xlsx, .csv, .docx, .txt |
| API key needed | No | Yes (Anthropic) |
| Token cost | Zero | Haiku per-parse call |
| Best for | Structured, repeatable tasks | Flexible, free-form instructions |

Both versions share the same Drive layout and prefix-based routing.

---

## File naming convention

    WSC{server}_{major}_{minor}_{YYYYMMDD}_{description}.ext

Example: WSC1_1_8_20260506_disk_audit.xlsx

The filename without extension becomes the task name used in output paths.

## Output structure

    WHISKY_OUT/
    └── WSC1_1_8_20260506_disk_audit/
        ├── WSC1_1_8_20260506_disk_audit.xlsx    copy of input
        ├── WSC1_1_8_20260506_disk_audit.csv     Command | Output results
        └── result/                               files created during task

## Input tips

**Google Sheets:** wrap paths and arguments in  to survive CSV quoting.

**Google Docs:** use single-quoted echo for file writes; verify with cat before compiling.
Avoid backslash-n in string arguments — the Docs to shell pipeline strips escape sequences.

## Configuration

Each version has a  in its directory. Key variables:

-  — Drive prefix this instance watches (unique per server)
-  — path to rclone Drive mount
-  — per-command timeout in seconds
-  — v1.8 only
-  — v1.8 only (default: claude-haiku-4-5-20251001)

## License

MIT
