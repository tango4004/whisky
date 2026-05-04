# User Guide (Human)

## What is Whisky?
Drop a Google Sheet with shell commands into your Drive root. Whisky runs them and returns a CSV.

## How to run a task

1. Go to the ROOT of your Google Drive (not in any subfolder).
2. Create a new Google Sheet there.
3. Enter shell commands in Column A, one per row, starting at A1. No header.
4. Name the file with the prefix for the target server:
     WS1_1_7_ -> ARM1
     WSC_1_7_ -> ARM2
     WS2_1_7_ -> AMD1
     WS3_1_7_ -> AMD2
   Example: WSC_1_7_mytest
5. Results appear in: WHISKY_OUT/WSC_1_7_mytest/WSC_1_7_mytest.csv

## Example (Column A)
date
uptime
ls -la ~

## Notes
- Plain text only.
- File must be in Drive root.
- Input sheet is deleted after successful processing.
- Re-running the same task name overwrites previous output (no leftover archive folders).
