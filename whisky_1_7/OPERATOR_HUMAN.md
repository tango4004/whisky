# Operator Guide (Human)

## Setup
1. Clone repo, create whisky_drive/ and work/ directories.
2. pip install pandas openpyxl
3. Copy whisky_1_7/.env.example to whisky_1_7/.env and set WHISKY_PREFIX for this server.
4. Mount Drive: rclone mount gdrive: whisky_drive/ --allow-other --vfs-cache-mode writes
5. Start: python3 whisky_1_7/whisky_1_7.py  (or use systemd service)

## .env settings (whisky_1_7/.env, gitignored)

WHISKY_PREFIX=WSC_1_7_        # unique per server - NEVER share across instances
WHISKY_IO_DIR=/home/whisky/whisky_drive
WHISKY_CMD_TIMEOUT=600

Two instances with the same prefix will both process the same task, causing duplicate output.

## Server prefix assignments

ARM1: WS1_1_7_  |  ARM2: WSC_1_7_  |  AMD1: WS2_1_7_  |  AMD2: WS3_1_7_

## Monitoring

- Log: whisky_1_7/whisky_1_7.log
- Watcher polls every 2 s
- Re-run of same task name overwrites previous output (no _OLD_ archive folders)
- sudo systemctl status whisky
