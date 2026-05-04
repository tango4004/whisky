# Operator Guide (AI / Bot)

## Server prefix assignments

ARM1: WS1_1_7_  |  ARM2: WSC_1_7_  |  AMD1: WS2_1_7_  |  AMD2: WS3_1_7_

Use the prefix that matches the target server.

## Dropping a task

Place an .xlsx file in IO_DIR (Drive root):

    <PREFIX><TASK_NAME>.xlsx
    Example: WSC_1_7_20260504_A1.xlsx

Column A: one shell command per row, no header.

## Validation checklist

- Filename starts with the correct prefix for the target server
- Extension is .xlsx
- Column A: commands only, no header, no empty leading rows

## Reading results

    WHISKY_OUT/<task_name>/<task_name>.csv
    Columns: Command, Output

Re-submitting the same task name overwrites the previous output - no _OLD_ folders.

## Error tokens in Output column

!!! TIMEOUT ERROR (600s) !!!   - command exceeded timeout
!!! SYSTEM ERROR: <msg> !!!    - unexpected exception
