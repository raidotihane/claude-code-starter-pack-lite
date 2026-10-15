"""PostToolUse hook: formats a Python file with ruff after Claude edits it.

Does nothing if the file isn't Python or ruff isn't installed (pip install ruff).
"""
import json
import shutil
import subprocess
import sys

path = (json.load(sys.stdin).get("tool_input", {}) or {}).get("file_path", "")
if path.endswith(".py") and shutil.which("ruff"):
    subprocess.run(["ruff", "format", "--quiet", path], check=False)
