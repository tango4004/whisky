# User Guide (AI / Bot)

## Task file naming convention

Use the mandatory prefix followed by a unique identifier:

```
WSC_1_7_[ISO_8601_DATE]_[UUID]
```

Example: `WSC_1_7_20260502_A3`

## File format

- **Type:** Google Sheets (Native)
- **Structure:** Single sheet, no header row.
- **Column A:** One shell command per cell (A1, A2, etc.).
- **Important:** Use PLAIN TEXT only. Do not use HTML tags or rich formatting inside cells.

## Workflow

1. Create a Google Sheet using the naming convention above.
2. Write commands as a simple string into Column A.
3. Avoid complex nested quotes (e.g., `echo "text"`) if the parser is sensitive; prefer simple strings for testing.
4. Poll the directory `WHISKY_OUT/<task_name>/<input_filename>.csv` for the output.

## Operational Tips

- Do not use temporary files (.xlsx). Create the Google Sheet directly.
- The system recognizes the task as soon as the file with the `WSC_1_7_` prefix is created in a reachable folder.
- Output CSV structure: `cmd,result`
