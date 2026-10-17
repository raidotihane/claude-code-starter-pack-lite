# Hooks

Hooks are commands Claude Code runs automatically before or after it uses a tool. These three make Claude safer and tidier without you having to remember anything.

| Hook | When | What it does |
|---|---|---|
| **Dangerous-command guard** | Before every shell command | Blocks `rm -rf /`, `rm -rf ~`, `rm -rf *`, `rm -rf ./`, force pushes (`--force-with-lease` is allowed), `git reset --hard`, skipping git hooks with `--no-verify`, and `curl ... \| sh` |
| **Self-protection** (part of the guard) | Before Claude edits a file | Stops Claude from editing `.claude/settings*` or anything in `.claude/hooks/`, so it can't switch the guard off. Reading them is fine |
| **Secrets guard** | Before reading, editing or running anything that touches `.env` | Keeps API keys in `.env` / `.env.local` / `.env.production` out of Claude's context. `.env.example` is allowed |
| **Python auto-format** | After Claude edits a `.py` file | Runs `ruff format` on that file (skipped if ruff isn't installed) |

When a guard blocks something, Claude sees the reason and asks you to do it yourself.

## Install

1. Copy `guard.py` and `format.py` into your project at `.claude/hooks/`.
2. Merge the `"hooks"` block from `settings.json` into your project's `.claude/settings.json` (create the file if it doesn't exist).
3. On macOS/Linux, if `python` isn't on your PATH, change `python` to `python3` in both commands.
4. Optional: `pip install ruff` for auto-formatting.
5. Restart Claude Code, then check the hooks are listed with `/hooks`.

## Test it

Ask Claude: *"Run `git reset --hard`."* It should report that the guard hook blocked it.

Or test the guard directly from your project folder:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"git reset --hard"}}' | python .claude/hooks/guard.py
```

It should print a "Blocked by guard hook" message (exit code 2).

## Customize

Add your own patterns to `BLOCKED_COMMANDS` in `guard.py`. Each entry is a regular expression and a reason. Example: block deploys to production with `(r"deploy\s+--prod", "production deploy")`.

The guard is a safety net, not a sandbox. A determined command can get around regex checks, so keep using Claude Code's permission prompts for anything risky.
