# whisky_1_7.py
# Whisky Project v1.7.4
#
# Author:  tango4004
# License: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the \Software\), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED \AS IS\, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import time
import shutil
import logging
import subprocess
import pandas as pd
from datetime import datetime

# --- LOAD .env (optional, overrides defaults) ---
_env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_file):
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

# --- DYNAMIC PATH SETUP ---
# Script resolves its own location and builds the directory tree from the project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

IO_DIR = os.environ.get("WHISKY_IO_DIR", "/home/whisky/whisky_drive")
OUT_DIR = os.path.join(IO_DIR, "WHISKY_OUT")
WORK_BASE = os.path.join(BASE_DIR, "work")

PREFIX = os.environ.get("WHISKY_PREFIX", "WSC_1_7_")
CMD_TIMEOUT = int(os.environ.get("WHISKY_CMD_TIMEOUT", "600"))

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()   # systemd appends stdout to log file
    ]
)

def get_ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def process_task(file_name):
    ts = get_ts()
    task_name = file_name.replace(".xlsx", "")
    local_dir = os.path.join(WORK_BASE, task_name)
    cloud_dir = os.path.join(OUT_DIR, task_name)
    src_path = os.path.join(IO_DIR, file_name)

    logging.info(f"--- Captured Task: {task_name} ---")

    try:
        # 1. CLEANUP (drop old run — no OLD folders, prevents Drive flood)
        for d in [local_dir, cloud_dir]:
            if os.path.exists(d):
                shutil.rmtree(d)
                logging.info(f"Removed old directory: {os.path.basename(d)}")

        # 2. STRUCTURE INIT
        tmp_dir = os.path.join(local_dir, "tmp")
        res_dir = os.path.join(local_dir, "result")
        os.makedirs(tmp_dir, exist_ok=True)
        os.makedirs(res_dir, exist_ok=True)
        os.makedirs(cloud_dir, exist_ok=True)

        # 3. MATERIALIZATION (copy input to local workspace and cloud mirror)
        local_xlsx = os.path.join(local_dir, file_name)
        shutil.copy2(src_path, local_xlsx)                              # local copy
        shutil.copy2(local_xlsx, os.path.join(cloud_dir, file_name))   # cloud mirror

        # 4. COMMAND PARSING
        df = pd.read_excel(local_xlsx, header=None)
        tasks = df[0].dropna().astype(str).tolist()
        results = []

        # 5. EXECUTION LOOP
        for cmd in tasks:
            cmd = cmd.strip()
            logging.info(f"Executing: {cmd[:50]}...")

            env = os.environ.copy()
            env["TMP_DIR"] = tmp_dir

            try:
                proc = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True,
                    cwd=local_dir, env=env, timeout=CMD_TIMEOUT
                )
                output = proc.stdout + proc.stderr
            except subprocess.TimeoutExpired as te:
                # Capture whatever output was collected before timeout
                out_part = (te.stdout if te.stdout else "") + (te.stderr if te.stderr else "")
                output = f"!!! TIMEOUT ERROR ({CMD_TIMEOUT}s) !!!\n--- Captured Output ---\n{out_part}"
                logging.warning(f"Command timed out: {cmd[:30]}")
            except Exception as e:
                output = f"!!! SYSTEM ERROR: {str(e)} !!!"
                logging.error(f"Execution failed: {e}")

            results.append([cmd, output])

        # 6. FINALIZATION (UTF-8-SIG for correct Excel opening)
        res_df = pd.DataFrame(results, columns=["Command", "Output"])
        local_res_csv = os.path.join(local_dir, f"{task_name}.csv")
        res_df.to_csv(local_res_csv, index=False, encoding='utf-8-sig')

        # 7. EXPORT RESULTS
        shutil.copy2(local_res_csv, os.path.join(cloud_dir, f"{task_name}.csv"))
        if os.path.exists(res_dir) and os.listdir(res_dir):
            shutil.copytree(res_dir, os.path.join(cloud_dir, "result"), dirs_exist_ok=True)

        # 8. CLEANUP INPUT (only after successful completion)
        if os.path.exists(src_path):
            os.remove(src_path)

        logging.info(f"Task {task_name} successfully finished.")

    except Exception as e:
        logging.critical(f"Critical error during {task_name} processing: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    # Validate environment before starting
    critical_paths = [IO_DIR, WORK_BASE]
    for p in critical_paths:
        if not os.path.exists(p):
            logging.error(f"Path not found: {p}. Create it before running.")
            exit(1)

    logging.info(f"Whisky v.1.7.4 started. Watcher active on: {IO_DIR}")

    while True:
        try:
            # Pick up only files matching our version prefix
            files = [f for f in os.listdir(IO_DIR) if f.startswith(PREFIX) and f.endswith(".xlsx")]
            for f in files:
                process_task(f)
        except Exception as e:
            logging.error(f"Main loop error: {e}")

        time.sleep(2)  # be gentle on CPU and disk I/O
