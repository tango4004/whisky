# User Guide (Human)

## What is Whisky?
A simple task runner: you drop an Excel file into a shared folder, and Whisky executes the commands inside and gives you the results.

## How to run a task
1. Create a `.xlsx` file - one shell command per row in column A, no header
2. Name it with the prefix `WSC_1_7_`, for example: `WSC_1_7_my_task.xlsx`
3. Drop it into the `whisky_drive/` folder (Google Drive mount or direct)
4. Wait a few seconds - results appear in `whisky_drive/WHISKY_OUT/WSC_1_7_my_task/RES_tasks.csv`

## Example file contents (column A)
```
echo hello from whisky
python3 --version
```

Expected output in RES_tasks.csv:
```
cmd,result
echo hello from whisky,hello from whisky
python3 --version,Python 3.12.3
```

## Notes
- The input file is deleted after successful processing
- Failed commands still produce output (exit code and stderr are captured)
