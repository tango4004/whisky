# Operator Guide (AI / Bot)

## Role
You manage the Whisky task queue programmatically.

## Dropping a task
Place a `.xlsx` file in `IO_DIR` with the naming convention:

    WSC_1_7_[TASK_NAME].xlsx

Each row in column A must contain one shell command (no header row).

## Validation checklist before dropping
- [ ] Filename starts with `WSC_1_7_`
- [ ] Extension is `.xlsx` (not .xls, .csv, etc.)
- [ ] Column A contains commands, one per row
- [ ] No empty leading rows

## Reading results
After the watcher processes the file, results appear in:

    IO_DIR/WHISKY_OUT/[TASK_NAME]/RES_tasks.csv

Columns: `cmd`, `result`

## Error handling
- `TIMEOUT` - command exceeded 600 s
- `ERROR: <msg>` - unexpected exception
