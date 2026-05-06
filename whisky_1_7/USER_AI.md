# Whisky v1.7 — AI Operator Guide

## Overview

Hardcoded bash task runner. No AI model involved.
Reads commands literally from spreadsheet cells, executes via subprocess, returns CSV.

## File naming convention

    PREFIX + DATE + DESCRIPTION + .ext

- PREFIX: unique per server instance, set in .env (e.g. WSC1_1_7_)
- DATE: YYYYMMDD recommended
- DESCRIPTION: alphanumeric and underscores only
- ext: .xlsx or .csv

The full filename minus extension is the task name used in all output paths.

## Input formats

- .xlsx: column A, no header (pandas read_excel)
- .csv: first column, UTF-8-BOM safe (stdlib csv reader)

## Output structure on Google Drive

    WHISKY_IO_DIR/
    ├── WSC1_1_7_<date>_<desc>.xlsx        input file, deleted on success
    └── WHISKY_OUT/
        └── WSC1_1_7_<date>_<desc>/
            ├── WSC1_1_7_<date>_<desc>.xlsx    copy of input
            ├── WSC1_1_7_<date>_<desc>.csv     Command | Output (UTF-8-BOM)
            └── result/                         files written during execution

## Quoting issues

Google Sheets CSV export doubles internal quote characters.
Wrap commands with paths or arguments in bash -c:

    bash -c "cp /tmp/file /home/whisky/"

Backslash-n inside string literals does not survive Sheets to shell.
Use && chaining for multi-step commands.

## No AI in v1.7

v1.7 reads commands literally. For Claude-assisted parsing, use v1.8.
