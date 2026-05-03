# User Guide (AI / Bot)

## Task file naming convention
Use ISO 8601 date and a UUID to avoid collisions:

    WSC_1_7_[ISO_8601_DATE]_[UUID].xlsx

Example: `WSC_1_7_20260427_a3f9c1.xlsx`

## File format
- Single sheet, no header row
- Column A: one shell command per row
- Encoding: UTF-8 (pandas default)

## Workflow
1. Generate the xlsx with `openpyxl` or `pandas`
2. Write it atomically (write to tmp, then rename) to avoid partial reads
3. Poll `OUT_DIR/WHISKY_OUT/<task_name>/RES_tasks.csv` until it appears
4. Parse CSV: columns `cmd` and `result`

## Python snippet

```python
import openpyxl, shutil, os

def drop_task(commands, io_dir, task_name):
    fname = \WSC_1_7_\ + task_name + \.xlsx
    tmp_path = os.path.join(io_dir, \.\ + fname)
    final_path = os.path.join(io_dir, fname)
    wb = openpyxl.Workbook()
    ws = wb.active
    for cmd in commands:
        ws.append([cmd])
    wb.save(tmp_path)
    shutil.move(tmp_path, final_path)
    return final_path
```
