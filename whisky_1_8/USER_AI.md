# Whisky v1.8 — AI Operator Guide

## Overview

All input files are routed through Claude (Haiku) for command extraction.
No hardcoded format assumptions — Claude reads the content and returns shell commands.
The watcher executes them via subprocess and returns results as CSV.

## File naming convention

    PREFIX + DATE + DESCRIPTION + .ext

- PREFIX: unique per server instance, set in .env (e.g. WSC1_1_8_)
- DATE: YYYYMMDD recommended
- DESCRIPTION: alphanumeric and underscores
- ext: .xlsx, .csv, .docx, .txt

The full filename minus extension is the task name used in all output paths.

## Input formats

- .xlsx: text extracted via openpyxl (extract_text.py)
- .csv: text extracted row by row
- .docx: text extracted via zipfile + xml parse
- .txt: read directly

Extracted text is sent to Claude as a single prompt. Claude returns one command per line.

## Output structure on Google Drive

    WHISKY_IO_DIR/
    ├── WSC1_1_8_<date>_<desc>.<ext>     input file, deleted on success
    └── WHISKY_OUT/
        └── WSC1_1_8_<date>_<desc>/
            ├── WSC1_1_8_<date>_<desc>.<ext>    copy of input
            ├── WSC1_1_8_<date>_<desc>.csv      Command | Output (UTF-8-BOM)
            └── result/                          files written during execution

## Claude parser (claude_parser.py)

- Calls Anthropic API (model set via CLAUDE_PARSER_MODEL in .env)
- Returns: one bash command per line, or "no commands found" if nothing found
- On empty/error response: task is skipped, input file preserved

## Quoting issues

Google Sheets CSV export doubles internal quote characters.
Always wrap commands with paths or arguments in bash -c:

    bash -c "cp /tmp/file /home/whisky/"

In Docs: backslash-n inside string literals does not survive the pipeline.
Use single-quoted echo for file writes; verify with cat before compiling.

## Token cost

One Haiku API call per file processed. Input: extracted text + system prompt (~500-2000 tokens).
Output: list of commands (~100-500 tokens). See Anthropic console for actual usage.
