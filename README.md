# Whisky Project

A lightweight task-runner that watches a Google Drive-mounted directory for Google Sheets, executes shell commands listed inside each sheets, and writes results back as CSV files.

## How it works

1. Drop a Google Sheets or `.xlsx` file prefixed `WSC_1_7_` into the watched input directory (root of Google Drive).
2. The watcher picks it up, reads one shell command per row, and runs them in order
3. Results land in `/WHISKY_OUT/<task_name>/<filename_without_ext>.csv` on Google Drive.
4. The input file is removed on success.

## Project layout

```
whisky_1_7/    application source and docs.
work/          temporary task workspace (auto-created, gitignored).
whisky_drive/  Google Drive mount point on server side (not in repo).
```

## Quick start

```bash
cd whisky_1_7
python3 whisky_1_7.py
```

## Requirements

- Python 3.8+.
- `pandas`, `openpyxl`.
- Google Drive mounted at `whisky_drive/` (e.g. via rclone).
