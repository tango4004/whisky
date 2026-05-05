#!/usr/bin/env python3
"""claude_parser.py - extract bash commands from any file via Anthropic API (Haiku).
Usage: claude_parser.py <file_path>
Output: one bash command per line, or: команда не распознана
"""
import sys, os, json, urllib.request, subprocess, shutil

# Load .env from same directory
_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env):
    with open(_env) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

API_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL    = os.environ.get("CLAUDE_PARSER_MODEL", "claude-haiku-4-5-20251001")
SYSTEM   = os.environ.get("CLAUDE_PARSER_SYSTEM",
    "Extract ALL bash/shell commands from the text below. "
    "Output each command on its own line. "
    "No markdown, no code blocks, no explanations, no line numbers. "
    "Just raw commands, one per line. "
    "If no bash commands are found, output exactly: команда не распознана")
EXTRACT  = os.environ.get("WHISKY_EXTRACT_SCRIPT",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract_text.py"))

def extract_text(path):
    try:
        r = subprocess.run(["python3", EXTRACT, path],
                           capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except Exception as e:
        print(f"extract error: {e}", file=sys.stderr)
        return ""

def call_claude(text):
    if not API_KEY:
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        return "команда не распознана"
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 1024,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": text}]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read())
        return data["content"][0]["text"].strip() or "команда не распознана"
    except Exception as e:
        print(f"API error: {e}", file=sys.stderr)
        return "команда не распознана"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: claude_parser.py <file>")
    path = sys.argv[1]
    if not os.path.exists(path):
        print("команда не распознана")
        sys.exit(0)
    text = extract_text(path)
    if not text:
        print("команда не распознана")
        sys.exit(0)
    print(call_claude(text))
