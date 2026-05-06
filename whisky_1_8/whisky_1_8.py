#!/usr/bin/env python3
# whisky_1_8.py
# Whisky Project v1.8.0
#
# Author:  tango4004
# License: MIT
#
# Smart parser edition: any file format -> Claude API (Haiku) -> bash commands -> execute -> results.
# No hardcoded format assumptions. Drop a file on Drive, get results back.

import os, time, shutil, logging, subprocess
from datetime import datetime

# --- LOAD .env ---
_env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_file):
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
BASE_DIR     = os.path.dirname(SCRIPT_DIR)

IO_DIR       = os.environ.get("WHISKY_IO_DIR",      "/home/whisky/whisky_drive")
OUT_DIR      = os.path.join(IO_DIR, "WHISKY_OUT")
WORK_BASE    = os.path.join(BASE_DIR, "work")
PREFIX       = os.environ.get("WHISKY_PREFIX",       "WS8_")
CMD_TIMEOUT  = int(os.environ.get("WHISKY_CMD_TIMEOUT", "600"))
CLAUDE_PARSER = os.environ.get("WHISKY_CLAUDE_PARSER",
                               os.path.join(SCRIPT_DIR, "claude_parser.py"))

SUPPORTED_EXT = (".xlsx", ".csv", ".docx", ".txt")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def get_ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def parse_commands(local_path):
    """Parse any file via Claude API -> list of bash commands."""
    try:
        r = subprocess.run(
            ["python3", CLAUDE_PARSER, local_path],
            capture_output=True, text=True, timeout=180
        )
        if r.stderr:
            logging.warning(f"Parser stderr: {r.stderr.strip()[:200]}")
        lines = [l.strip() for l in r.stdout.splitlines() if l.strip()]
        if not lines or lines[0] == "команда не распознана":
            return []
        return lines
    except Exception as e:
        logging.error(f"Parser error: {e}")
        return []

def process_task(file_name):
    task_name = file_name.rsplit(".", 1)[0]
    local_dir  = os.path.join(WORK_BASE, task_name)
    cloud_dir  = os.path.join(OUT_DIR, task_name)
    src_path   = os.path.join(IO_DIR, file_name)

    logging.info(f"--- Task: {task_name} ---")

    try:
        # Cleanup old run
        for d in [local_dir, cloud_dir]:
            if os.path.exists(d):
                shutil.rmtree(d)

        # Init dirs
        tmp_dir = os.path.join(local_dir, "tmp")
        res_dir = os.path.join(local_dir, "result")
        for d in [tmp_dir, res_dir, cloud_dir]:
            os.makedirs(d, exist_ok=True)

        # Materialize from rclone VFS
        local_file = os.path.join(local_dir, file_name)
        try:
            shutil.copy2(src_path, local_file)
        except OSError as e:
            logging.error(f"Cannot read {file_name}: {e}. Removing.")
            try: os.remove(src_path)
            except Exception: pass
            return
        # Check local copy is non-empty (file may not be synced yet)
        if os.path.getsize(local_file) == 0:
            logging.warning(f"Local copy of {file_name} is empty, skipping (not yet synced).")
            try: os.remove(local_file)
            except Exception: pass
            return

        # Mirror input to cloud
        ext = file_name.rsplit(".", 1)[-1].lower()
        if ext != "csv":
            shutil.copy2(local_file, os.path.join(cloud_dir, file_name))

        # Parse
        commands = parse_commands(local_file)
        if not commands:
            logging.warning(f"Task {task_name}: no commands found.")
            if os.path.exists(src_path): os.remove(src_path)
            return

        # Execute
        results = []
        env = os.environ.copy()
        env["TMP_DIR"] = tmp_dir

        failed = False
        for cmd in commands:
            if failed:
                results.append([cmd, "SKIPPED: previous command failed"])
                continue
            logging.info(f"Exec: {cmd[:60]}...")
            try:
                proc = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True,
                    cwd=local_dir, env=env, timeout=CMD_TIMEOUT
                )
                output = proc.stdout + proc.stderr
                if proc.returncode != 0:
                    logging.warning(f"Command failed (rc={proc.returncode}): {cmd[:40]}")
                    failed = True
            except subprocess.TimeoutExpired as te:
                out_part = (te.stdout or "") + (te.stderr or "")
                output = f"TIMEOUT ({CMD_TIMEOUT}s)" + chr(10) + out_part
                logging.warning(f"Timeout: {cmd[:40]}")
                failed = True
            except Exception as e:
                output = f"ERROR: {e}"
                logging.error(f"Exec failed: {e}")
                failed = True
            results.append([cmd, output])

        # Write results CSV
        import csv
        local_csv = os.path.join(local_dir, f"{task_name}.csv")
        with open(local_csv, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["Command", "Output"])
            w.writerows(results)

        # Export to Drive
        shutil.copy2(local_csv, os.path.join(cloud_dir, f"{task_name}.csv"))
        if os.listdir(res_dir):
            shutil.copytree(res_dir, os.path.join(cloud_dir, "result"), dirs_exist_ok=True)

        # Update WHISKY_INDEX.csv in Drive root
        import datetime
        index_path = os.path.join(IO_DIR, "WHISKY_INDEX.csv")
        status = "FAILED" if failed else "OK"
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        details = f"WHISKY_OUT/{task_name}/{task_name}.csv" if failed else ""
        index_row = [ts, task_name, status, len(results), details]
        write_header = not os.path.exists(index_path)
        with open(index_path, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["Timestamp", "Task", "Status", "Commands", "Details"])
            w.writerow(index_row)

        # Remove input
        if os.path.exists(src_path): os.remove(src_path)
        logging.info(f"Task {task_name} done. {len(results)} command(s).")

    except Exception as e:
        logging.critical(f"Critical error in {task_name}: {e}")

# --- MAIN ---
if __name__ == "__main__":
    for p in [IO_DIR, WORK_BASE]:
        if not os.path.exists(p):
            logging.error(f"Required path missing: {p}")
            exit(1)

    logging.info(f"Whisky v1.8.0 started. PREFIX={PREFIX}, watching: {IO_DIR}")

    while True:
        try:
            files = [
                f for f in os.listdir(IO_DIR)
                if f.startswith(PREFIX) and f.endswith(SUPPORTED_EXT)
            ]
            for f in files:
                process_task(f)
        except Exception as e:
            logging.error(f"Main loop error: {e}")
        time.sleep(2)
