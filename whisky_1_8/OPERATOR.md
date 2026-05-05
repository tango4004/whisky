# Whisky v1.8 — Operator Guide

## Requirements

- Python 3.8+
-  ()
-  or stdlib zipfile (built-in fallback used)
- rclone mounted Google Drive at 
- Anthropic API key with access to claude-haiku-4-5-20251001

## Deployment

1. Clone the repo and navigate to 
2. Copy  to  and fill in values
3. Each server instance must have a **unique** 
4. Run as a systemd service (see example below)

## Systemd service

    [Unit]
    Description=Whisky v1.8
    After=network.target

    [Service]
    Type=simple
    User=whisky
    WorkingDirectory=/home/whisky/whisky-project/whisky_1_8
    ExecStart=/usr/bin/python3 whisky_1_8.py
    Restart=on-failure
    RestartSec=10
    StandardOutput=append:/home/whisky/whisky-project/whisky_1_8/whisky_1_8.log
    StandardError=append:/home/whisky/whisky-project/whisky_1_8/whisky_1_8.log

    [Install]
    WantedBy=multi-user.target

## Output structure

For each task  the watcher creates:

    WHISKY_OUT/
    └── WS8_<date>_<name>/
        ├── WS8_<date>_<name>.<ext>   # copy of input
        ├── WS8_<date>_<name>.csv     # Command | Output results
        └── result/                   # any files written during execution

## Security notes

- Commands run as the service user — scope permissions accordingly
-  is gitignored; never commit API keys
- There is no command allowlist in v1.8.0 — smoke test only
