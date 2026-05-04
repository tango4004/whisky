# whisky_1_8.py
# Whisky Project v1.8.0
#
# Author:  tango4004
# License: MIT
#
# Changes from v1.7: adds .docx support — one command per paragraph.

import os
import re as _re
import time
import shutil
import logging
import zipfile
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(SCRIPT_DIR)

IO_DIR       = os.environ.get("WHISKY_IO_DIR",      "/home/whisky/whisky_drive")
OUT_DIR      = os.path.join(IO_DIR, "WHISKY_OUT")
WORK_BASE    = os.path.join(BASE_DIR, "work")
PREFIX       = os.environ.get("WHISKY_PREFIX",      "WSC_1_8_")
CMD_TIMEOUT  = int(os.environ.get("WHISKY_CMD_TIMEOUT", "600"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(SCRIPT_DIR, "whisky_1_8.log")),
        logging.StreamHandler()
    ]
)

def get_ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _parse_docx(path):
    """Extract commands from .docx — one command per paragraph."""
    tmp = path + "._tmp"
    shutil.copy2(path, tmp)   # materialize from rclone VFS
    try:
        with zipfile.ZipFile(tmp) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        paragraphs = _re.findall(r"<w:p[ >].*?</w:p>", xml, _re.DOTALL)
        cmds = []
        for p in paragraphs:
            text = _re.sub(r"<[^>]+>", " ", p)
            text = " ".join(text.split())
            if text:
                cmds.append(text)
        return cmds
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

def _parse_xlsx(path):
    """Extract commands from .xlsx column A."""
    df = pd.read_excel(path, header=None)
    return df[0].dropna().astype(str).str.strip().tolist()

def process_task(file_name):
    ts = get_ts()
    task_name  = file_name.rsplit(".", 1)[0]
    local_dir  = os.path.join(WORK_BASE, task_name)
    cloud_dir  = os.path.join(OUT_DIR, task_name)
    src_path   = os.path.join(IO_DIR, file_name)
    ext        = file_name.rsplit(".", 1)[-1].lower()

    logging.info(f"--- Captured Task: {task_name} ({ext}) ---")

    try:
        # 1. CLEANUP old run
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

        # 3. MATERIALIZATION
        local_src = os.path.join(local_dir, file_name)
        shutil.copy2(src_path, local_src)
        shutil.copy2(local_src, os.path.join(cloud_dir, file_name))

        # 4. COMMAND PARSING
        if ext == "docx":
            tasks = _parse_docx(local_src)
        else:
            tasks = _parse_xlsx(local_src)

        results = []

        # 5. EXECUTION LOOP
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
                output = f"!!! TIMEOUT ERROR ({CMD_TIMEOUT}s) !!!
{out_part}"
                logging.warning(f"Timeout: {cmd[:40]}")
            except Exception as e:
                output = f"!!! SYSTEM ERROR: {e} !!!"
                logging.error(f"Execution failed: {e}")
            results.append([cmd, output])

        # 6. FINALIZATION
        res_df = pd.DataFrame(results, columns=["Command", "Output"])
        local_csv = os.path.join(local_dir, f"{task_name}.csv")
        res_df.to_csv(local_csv, index=False, encoding="utf-8-sig")

        # 7. EXPORT
        shutil.copy2(local_csv, os.path.join(cloud_dir, f"{task_name}.csv"))
        if os.path.exists(res_dir) and os.listdir(res_dir):
            shutil.copytree(res_dir, os.path.join(cloud_dir, "result"), dirs_exist_ok=True)

        # 8. CLEANUP INPUT
        if os.path.exists(src_path):
            os.remove(src_path)

        logging.info(f"Task {task_name} done.")

    except Exception as e:
        logging.critical(f"Critical error in {task_name}: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    for p in [IO_DIR, WORK_BASE]:
        if not os.path.exists(p):
            logging.error(f"Path not found: {p}. Create it before running.")
            exit(1)

    logging.info(f"Whisky v1.8.0 started. Watching: {IO_DIR} prefix={PREFIX}")

    while True:
        try:
            files = [
                f for f in os.listdir(IO_DIR)
                if f.startswith(PREFIX) and f.endswith((".xlsx", ".docx"))
            ]
            for f in files:
                process_task(f)
        except Exception as e:
            logging.error(f"Main loop error: {e}")
        time.sleep(2)
