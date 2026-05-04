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

## Server prefix assignments

| Server   | Prefix      |
|----------|-------------|
| server_c | WSC_1_7_    |
| server_1 | WS1_1_7_    |
| server_2 | WS2_1_7_    |
| server_3 | WS3_1_7_    |

## Monitoring

- Log: whisky_1_7/whisky_1_7.log
- Watcher polls every 2 s
- Re-run of same task name overwrites previous output (no _OLD_ archive folders)
- sudo systemctl status whisky
