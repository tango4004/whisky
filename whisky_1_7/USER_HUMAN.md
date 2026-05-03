# User Guide (Human)

## What is Whisky?
A simple task runner: you create a Google Sheet, Whisky executes the commands inside and gives you the results.

## How to run a task
1. Go to the **root (main) folder** of your Google Drive.
2. Create a new Google Sheet right there (do not place it in subfolders unless instructed).
3. Enter your shell commands in Column A (one command per row, starting from A1). No headers.
4. Name the file with the prefix WSC_1_7_, for example: WSC_1_7_my_task
5. Wait a few seconds — results appear in the folder: WHISKY_OUT/WSC_1_7_my_task/WSC_1_7_my_task.csv

## Example Sheet contents (Column A)
- A1: date
- A2: uptime
- A3: ls -la

## Notes
- Use plain text only.
- Important: The file must be created in the **Root of Google Drive**.
- The input Google Sheet is deleted after successful processing.
