# Whisky Project

A lightweight Drive-connected task runner for servers with AI agents.
Drop a file on Google Drive — get shell command results back as CSV.

## Versions

**v1.7** — for servers without an AI agent. Reads commands directly from .xlsx cells.
Optionally uses Gemini CLI ( prefix) for command extraction from any file format.

**v1.8** — for servers with an Anthropic API key. Routes all input files through
Claude (Haiku) for command extraction, then executes results. Supports .xlsx, .csv, .docx, .txt.

## How it works

1. Drop a file with the configured prefix into the Drive root (e.g. ).
2. The watcher picks it up, sends the file contents to Claude for command extraction.
3. Extracted shell commands run in order on the server.
4. Results land in  on Drive.
5. The input file is removed on success.

## Quick start (v1.8)

    cd whisky_1_8
    cp .env.example .env
    # fill in ANTHROPIC_API_KEY and WHISKY_PREFIX
    python3 whisky_1_8.py

## Quick start (v1.7)

    cd whisky_1_7
    cp .env.example .env
    python3 whisky_1_7.py

## Input format tips

**Google Sheets (.xlsx):** wrap paths and arguments in  to avoid
CSV quoting issues. Example: 

**Google Docs (.docx):** preferred for multi-line scripts and file creation.
Use single-quoted  for code literals — avoids escape conflicts across
the Docs → connector → shell pipeline. Verify each write with {"jsonrpc":"2.0","method":"notifications/cancelled","params":{"requestId":115,"reason":"McpError: MCP error -32001: Request timed out"}} before compiling.

## Configuration

See  in each version directory.

Key variables for v1.8:

| Variable | Description |
|---|---|
|  | Drive prefix this instance watches (unique per server) |
|  | Path to rclone Drive mount |
|  | Anthropic API key for Claude parser |
|  | Model for extraction (default: claude-haiku-4-5-20251001) |

## License

MIT
