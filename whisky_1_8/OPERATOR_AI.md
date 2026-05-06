# Whisky v1.8 — Developer / AI Guide

## Architecture

All files go through claude_parser.py (Anthropic API, Haiku by default).
extract_text.py handles format-specific text extraction before the API call.
No pandas. No Gemini. No hardcoded format assumptions.

## Parse pipeline

    input file
        -> extract_text.py  (xlsx/csv/docx/txt -> plain text)
        -> claude_parser.py (text -> one bash command per line)
        -> subprocess.run() (each command, cwd=task workdir)
        -> results CSV

## Prefix routing

Each server instance has a unique WHISKY_PREFIX in .env.
Naming scheme: WSC{server}_{major}_{minor}_ (e.g. WSC1_1_8_, WSC2_1_8_).
Two instances must not share a prefix — both would process the same task.

## Known issues

- Haiku may return extra explanation text mixed with commands on complex inputs.
  Mitigation: system prompt instructs "one command per line, no explanation".
- Google Sheets CSV export doubles quotes — use bash -c wrapping.
- Backslash-n in Docs does not survive to shell — use single-quoted echo.
- On Gemini quota exhaustion (v1.7 only): not applicable here.

## Token logging

Not implemented in v1.8.0. Monitor usage via Anthropic console.
Model is configurable: CLAUDE_PARSER_MODEL in .env.
