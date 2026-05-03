# User Guide (Human)

## What is Whisky?
A simple task runner: you drop an Excel file into a shared folder, and Whisky executes the commands inside and gives you the results.

## How to run a task
1. Create a  file — one shell command per row in column A, no header
2. Name it with the prefix , for example:
   - 
3. Drop it into the  folder (Google Drive mount or direct)
4. Wait a few seconds — results appear in 

## Example file contents (column A)
hello from whisky
Python 3.12.3

## Notes
- The input file is deleted after successful processing
- Failed commands still produce output (exit code and stderr are captured)
