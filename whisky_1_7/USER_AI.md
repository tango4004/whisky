# Whisky v1.7 — AI Operator Guide

## Overview

Whisky v1.7 is a hardcoded bash task runner. It watches a Drive-mounted directory for
files with a configured prefix, reads shell commands from column A, executes them, and
writes results to CSV.

## Input formats

-  — one command per row, column A, no header
-   — one command per row, first column (UTF-8-BOM safe)

## Prefix routing

Each server instance watches a unique prefix (set in ).
Default: . Two instances must never share a prefix.

## Command encoding notes

**Google Sheets → CSV export** doubles internal quote characters.
Always wrap commands containing paths or arguments in :

    bash -c "df -h && uptime"

Do not rely on  inside string literals — the Sheets → connector → shell pipeline
does not preserve escape sequences. Use  chaining instead.

## Output

Results land in  with columns:
,  (stdout + stderr merged).

## No AI parsing in v1.7

v1.7 reads commands literally from cells. There is no AI model involved.
For AI-assisted command extraction from arbitrary file formats, use v1.8.
