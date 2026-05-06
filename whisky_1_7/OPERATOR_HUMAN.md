# Whisky v1.7 — Operator Guide

## Requirements

- Python 3.8+
- ,  ()
- rclone mounted Google Drive at 

## Setup

    cd whisky_1_7
    cp .env.example .env
    # set WHISKY_PREFIX (unique per server) and WHISKY_IO_DIR
    python3 whisky_1_7.py

## Systemd service

    [Unit]
    Description=Whisky v1.7 task runner
    After=network.target

    [Service]
    Type=simple
    User=whisky
    WorkingDirectory=/home/whisky/whisky_1_7
    ExecStart=/usr/bin/python3 /home/whisky/whisky_1_7/whisky_1_7.py
    Restart=on-failure
    RestartSec=10
    StandardOutput=append:/home/whisky/whisky_1_7/whisky_1_7.log
    StandardError=append:/home/whisky/whisky_1_7/whisky_1_7.log

    [Install]
    WantedBy=multi-user.target

## Configuration (.env)

    WHISKY_PREFIX=WSC1_1_7_      # unique per server instance
    WHISKY_IO_DIR=/home/whisky/whisky_drive
    WHISKY_CMD_TIMEOUT=600

## Output structure

    WHISKY_OUT/
    └── <task_name>/
        ├── <task_name>.<ext>   # copy of input file
        ├── <task_name>.csv     # Command | Output results
        └── result/             # files written during execution
