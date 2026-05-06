# Whisky v1.8 — Operator Guide

## Requirements

- Python 3.8+
- openpyxl: pip install openpyxl
- rclone mounted Google Drive at WHISKY_IO_DIR
- Anthropic API key

## Setup

    cd /home/whisky/whisky_1_8
    cp .env.example .env
    # fill in ANTHROPIC_API_KEY and WHISKY_PREFIX
    python3 whisky_1_8.py

## Systemd service

    [Unit]
    Description=Whisky v1.8
    After=network.target

    [Service]
    Type=simple
    User=whisky
    WorkingDirectory=/home/whisky/whisky_1_8
    ExecStart=/usr/bin/python3 /home/whisky/whisky_1_8/whisky_1_8.py
    Restart=on-failure
    RestartSec=10
    StandardOutput=append:/home/whisky/whisky_1_8/whisky_1_8.log
    StandardError=append:/home/whisky/whisky_1_8/whisky_1_8.log

    [Install]
    WantedBy=multi-user.target

> Note: WorkingDirectory is the deploy directory, not the git repo.
> Deploy by copying files from whisky-project/whisky_1_8/ to /home/whisky/whisky_1_8/.

## Configuration (.env)

    WHISKY_PREFIX=WSC1_1_8_
    WHISKY_IO_DIR=/home/whisky/whisky_drive
    WHISKY_CMD_TIMEOUT=600
    ANTHROPIC_API_KEY=sk-ant-api03-...
    CLAUDE_PARSER_MODEL=claude-haiku-4-5-20251001
    WHISKY_CLAUDE_PARSER=/home/whisky/whisky_1_8/claude_parser.py
    WHISKY_EXTRACT_SCRIPT=/home/whisky/whisky_1_8/extract_text.py

## Output structure

    WHISKY_OUT/
    └── <task_name>/
        ├── <task_name>.<ext>    copy of input
        ├── <task_name>.csv      Command | Output results
        └── result/              files written during execution
