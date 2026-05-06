# whisky_1_7.py
# Whisky Project v1.7.6
#
# Author:  tango4004
# License: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import csv
import time
import shutil
import logging
import subprocess
import pandas as pd
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
PREFIX       = os.environ.get("WHISKY_PREFIX",       "WSC1_1_7_")
CMD_TIMEOUT  = int(os.environ.get("WHISKY_CMD_TIMEOUT", "600"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def get_ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _parse_xlsx(path):
    """Extract commands from .xlsx — column A, no header."""
    df = pd.read_excel(path, header=None)
    return df[0].dropna().astype(str).tolist() if not df.empty and 0 in df.columns else []

def _parse_csv(path):
    """Extract commands from .csv — first column."""
    cmds = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if row and row[0].strip():
                cmds.append(row[0].strip())
    return cmds

def process_task(file_name):
    ts        = get_ts()
    task_name = file_name.rsplit(".", 1)[0]
    local_dir = os.path.join(WORK_BASE, task_name)
    cloud_dir = os.path.join(OUT_DIR, task_name)
    src_path  = os.path.join(IO_DIR, file_name)
    ext       = file_name.rsplit(".", 1)[-1].lower()

    logging.info(f"--- Task: {task_name} ---")

    try:
        for d in [local_dir, cloud_dir]:
            if os.path.exists(d):
                shutil.rmtree(d)

        tmp_dir = os.path.join(local_dir, "tmp")
        res_dir = os.path.join(local_dir, "result")
        for d in [tmp_dir, res_dir, cloud_dir]:
            os.makedirs(d, exist_ok=True)

        local_src = os.path.join(local_dir, file_name)
        try:
            shutil.copy2(src_path, local_src)
        except OSError as e:
            logging.error(f"Cannot read {file_name}: {e}. Removing to stop retry loop.")
            try: os.remove(src_path)
            except Exception: pass
            return

        if ext != "csv":
            shutil.copy2(local_src, os.path.join(cloud_dir, file_name))

        if ext == "csv":
            tasks = _parse_csv(local_src)
        else:
            tasks = _parse_xlsx(local_src)

        if not tasks:
            logging.warning(f"No commands found in {file_name}, skipping.")
            if os.path.exists(src_path): os.remove(src_path)
            return

        results = []
        for cmd in tasks:
            cmd = cmd.strip()
            if not cmd:
                continue
            logging.info(f"Executing: {cmd[:60]}...")
            env = os.environ.copy()
            env["TMP_DIR"] = tmp_dir
            try:
                proc = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True,
                    cwd=local_dir, env=env, timeout=CMD_TIMEOUT
                )
                output = proc.stdout + proc.stderr
            except subprocess.TimeoutExpired as te:
                out_part = (te.stdout or "") + (te.stderr or "")
                output = "TIMEOUT (%ds)" % CMD_TIMEOUT + chr(10) + out_part
                logging.warning(f"Timeout: {cmd[:40]}")
            except Exception as e:
                output = f"ERROR: {e}"
                logging.error(f"Execution failed: {e}")
            results.append([cmd, output])

        res_df = pd.DataFrame(results, columns=["Command", "Output"])
        local_csv = os.path.join(local_dir, f"{task_name}.csv")
        res_df.to_csv(local_csv, index=False, encoding="utf-8-sig")

        shutil.copy2(local_csv, os.path.join(cloud_dir, f"{task_name}.csv"))
        if os.path.exists(res_dir) and os.listdir(res_dir):
            shutil.copytree(res_dir, os.path.join(cloud_dir, "result"), dirs_exist_ok=True)

        if os.path.exists(src_path): os.remove(src_path)
        logging.info(f"Task {task_name} done.")

    except Exception as e:
        logging.critical(f"Critical error in {task_name}: {e}")

if __name__ == "__main__":
    for p in [IO_DIR, WORK_BASE]:
        if not os.path.exists(p):
            logging.error(f"Path not found: {p}")
            exit(1)

    logging.info(f"Whisky v1.7.6 started. PREFIX={PREFIX}, watching: {IO_DIR}")

    while True:
        try:
            files = [
                f for f in os.listdir(IO_DIR)
                if f.startswith(PREFIX) and f.endswith((".xlsx", ".csv"))
            ]
            for f in files:
                process_task(f)
        except Exception as e:
            logging.error(f"Main loop error: {e}")
        time.sleep(2)
