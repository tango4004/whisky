# User Guide (AI / Bot)

## Server prefix assignments

| Server   | Prefix      |
|----------|-------------|
| server_c | WSC_1_7_    |
| server_1 | WS1_1_7_    |
| server_2 | WS2_1_7_    |
| server_3 | WS3_1_7_    |

## Task file naming

    <PREFIX><ISO_DATE>_<ID>.xlsx
    Example (server_c): WSC_1_7_20260504_A1.xlsx

## File format

- Type: .xlsx
- Structure: single sheet, no header
- Column A: one shell command per cell (A1, A2, ...)
- Plain text only

## Workflow

1. Create .xlsx with commands in column A.
2. Place in root of watched Google Drive (not in a subfolder).
3. Poll WHISKY_OUT/<task_name>/<task_name>.csv for results.

## Output CSV

Column Command: the shell command that was run
Column Output:  combined stdout + stderr

## Notes

- Input file is deleted after successful processing.
- Re-submitting the same task name overwrites previous output (no archive copies).
