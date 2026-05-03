# Operator Guide (Human)

## Role
Deploy and maintain the Whisky watcher service on the server.

## Setup
1. Clone the repo into the project root
2. Create directories: `whisky_drive/` (input) and `work/` (workspace)
3. Install deps: `pip install pandas openpyxl`
4. Start: `python3 whisky_1_7/whisky_1_7.py`

## Key paths (edit in whisky_1_7.py if needed)
- `IO_DIR` - watched input directory (default: `/home/whisky/whisky_drive`)
- `OUT_DIR` - results output (`IO_DIR/WHISKY_OUT`)
- `WORK_BASE` - local task workspace (`<project_root>/work`)

## Monitoring
- Log file: `whisky_1_7/whisky_1_7.log`
- Watcher polls every 2 seconds
- Old task directories are archived as `<dir>_OLD_<timestamp>` before each run
