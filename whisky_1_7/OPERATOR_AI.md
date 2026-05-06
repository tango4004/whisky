# Whisky v1.7 — Developer / AI Guide

## Architecture

Hardcoded bash task runner. No AI model involved in command parsing.
Reads commands literally from spreadsheet cells and executes them via subprocess.

## Input formats

- .xlsx — column A, no header (parsed with pandas)
- .csv  — first column, UTF-8-BOM safe

## Prefix routing

Each server instance has a unique WHISKY_PREFIX in .env.
Only files starting with PREFIX are picked up. Two instances must not share a prefix.

## Known quoting issues

Google Sheets CSV export doubles internal quotation marks. To pass paths or arguments:
  Use: bash -c \df -h  Not: df -h /some/path  (may lose arguments after CSV round-trip)

Backslash-n inside string literals does not survive the Sheets to shell pipeline.
Use && chaining for multi-step commands, not newlines.

## No AI in v1.7

v1.7 contains no model calls. All command extraction is hardcoded.
For Claude-assisted parsing of arbitrary formats, see whisky_1_8.
