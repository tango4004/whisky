# User Guide (AI / Bot)

## Task file naming convention
Use ISO 8601 date and a UUID to avoid collisions:

    WSC_1_7_[ISO_8601_DATE]_[UUID].xlsx

Example: 

## File format
- Single sheet, no header row
- Column A: one shell command per row
- Encoding: UTF-8 (pandas default)

## Workflow
1. Generate the xlsx with  or 
2. Write it atomically (write to tmp, then rename) to avoid partial reads
3. Poll  until it appears
4. Parse CSV: columns  and 

## Python snippet

