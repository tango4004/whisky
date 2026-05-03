# Whisky Project

A lightweight task-runner that watches a Google Drive-mounted directory for Excel workbooks, executes shell commands listed inside each workbook, and writes results back as CSV files.

## How it works

1. Drop a .xlsx file prefixed WSC_1_7_ into the watched input directory (whisky_drive/)
2. The watcher picks it up, reads one shell command per row, and runs them in order
3. Results land in whisky_drive/WHISKY_OUT/<task_name>/RES_tasks.csv
4. The input file is removed on success

## Project layout

src/       application source
logs/      runtime logs
docs/      documentation
config/    config files
tests/     tests
work/      temporary task workspace (auto-created, gitignored)

## Quick start

cp .env.example .env
python3 src/whisky_1_7.py

## Requirements

- Python 3.8+
- pandas, openpyxl
- Google Drive mounted at whisky_drive/ (e.g. via rclone)
