# Whisky Project

A lightweight task-runner that watches a Google Drive-mounted directory for .xlsx files,
executes shell commands listed inside each file, and writes results back as CSV files.

## How it works

1. Drop an .xlsx file with the configured prefix (e.g. WSC_1_7_) into the Drive root.
2. The watcher picks it up, reads one shell command per row, and runs them in order.
3. Results land in WHISKY_OUT/<task_name>/<task_name>.csv on Google Drive.
4. The input file is removed on success.
5. Previous output for the same task name is overwritten (no _OLD_ archive copies).

## Quick start

    cd whisky_1_7 && cp .env.example .env && python3 whisky_1_7.py

## Configuration (.env)

WHISKY_PREFIX      - prefix this instance watches (unique per server)
WHISKY_IO_DIR      - path to Drive mount (default: /home/whisky/whisky_drive)
WHISKY_CMD_TIMEOUT - per-command timeout seconds (default: 600)

## Multi-server prefixes

ARM1: WS1_1_7_  |  ARM2: WSC_1_7_  |  AMD1: WS2_1_7_  |  AMD2: WS3_1_7_
