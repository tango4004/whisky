#!/bin/bash
# smart_parser.sh -- extract bash commands from any file format via Gemini CLI
# Usage: smart_parser.sh <local_file_path>
# Output: one bash command per line, or: команда не распознана

set -euo pipefail

FILE="$1"
EXTRACT_SCRIPT="${WHISKY_EXTRACT_SCRIPT:-/home/whisky/whisky-project/whisky_1_7/extract_text.py}"
DEFAULT_PROMPT="Extract ALL bash/shell commands from the text below. Output each command on its own line. No markdown, no code blocks, no explanations, no line numbers. Just raw commands, one per line. If no bash commands are found, output exactly: команда не распознана"
PROMPT="${WHISKY_EXTRACT_PROMPT:-$DEFAULT_PROMPT}"

if [ ! -f "$FILE" ]; then
    echo команда не распознана
    exit 0
fi

TEXT=$(python3 "$EXTRACT_SCRIPT" "$FILE" 2>/dev/null)

if [ -z "$TEXT" ]; then
    echo команда не распознана
    exit 0
fi

TMPFILE=$(mktemp /tmp/whisky_prompt.XXXXXX)
trap 'rm -f "$TMPFILE"' EXIT
printf '%s

%s
' "$PROMPT" "$TEXT" > "$TMPFILE"

RESULT=$(GEMINI_CLI_TRUST_WORKSPACE=true gemini --model gemini-2.0-flash -p "$(cat "$TMPFILE")" 2>/dev/null) || true

if [ -z "$RESULT" ]; then
    echo команда не распознана
    exit 0
fi

echo "$RESULT"
