"""PreToolUse hook: blocks destructive shell commands and access to .env secret files.

Claude Code sends the tool call as JSON on stdin. Exit code 2 blocks the call and
shows the stderr message to Claude, so it can explain or try another way.
"""
import json
import re
import sys
from pathlib import PurePath

BLOCKED_COMMANDS = [
    (r"\brm\s+(-[\w-]+\s+)*-\w*[rR]\w*(\s+-[\w-]+)*\s+(/|~|\$HOME|\*|\.)/?(?=\s|$|[\"';&|)])", "recursive delete of /, ~, * or the current folder"),
    (r"\bgit\s+push\b.*\s(--force(?![\w-])|-f\b)", "force push"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard (discards uncommitted work)"),
    (r"\b(curl|wget)\b[^|]*\|\s*(sudo\s+)?(ba|z)?sh\b", "piping a download straight into a shell"),
    (r"\bgit\s+(commit|push|merge)\b.*\s--no-verify\b|\bgit\s+commit\s+(-\w+\s+)*-n\b", "skipping git hooks with --no-verify"),
    (r"\.env\b(?!\.(example|sample|template)\b)", "touching a .env secrets file"),
]
SAFE_ENV_NAMES = {".env.example", ".env.sample", ".env.template"}


def check(payload):
    """Return a reason string if the tool call should be blocked, else None."""
    tool = payload.get("tool_name", "")
    args = payload.get("tool_input", {}) or {}
    if tool == "Bash":
        command = args.get("command", "")
        for pattern, reason in BLOCKED_COMMANDS:
            if re.search(pattern, command):
                return reason
    else:
        path = PurePath(args.get("file_path", ""))
        if tool != "Read" and ".claude" in path.parts and (path.name.startswith("settings") or "hooks" in path.parts):
            return "editing Claude Code's own hook or settings files"
        name = path.name
        if name == ".env" or (name.startswith(".env.") and name not in SAFE_ENV_NAMES):
            return "reading or editing a .env secrets file"
    return None


if __name__ == "__main__":
    reason = check(json.load(sys.stdin))
    if reason:
        print(f"Blocked by guard hook: {reason}. Ask the user to do this themselves if it's really needed.", file=sys.stderr)
        sys.exit(2)
