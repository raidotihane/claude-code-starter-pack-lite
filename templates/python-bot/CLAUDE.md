# [Project name]

[One sentence: what the bot does and for whom. Example: "Discord bot that posts a daily summary of new GitHub issues to #dev."]

## Commands
- Install: `python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt` (on macOS/Linux: `source .venv/bin/activate`)
- Run: `python -m [package]`
- Test: `pytest -q`
- Lint/format: `ruff check . && ruff format .`

## Layout
- `[package]/main.py`: entry point, starts the scheduler/event loop
- `[package]/handlers/`: one file per command or event
- `[package]/clients/`: wrappers for external APIs (one per service)
- `tests/`: mirrors the package layout

## Rules
- Config comes from environment variables loaded in `[package]/config.py`. Never hard-code tokens, and never read or print `.env`.
- Every external API call goes through `clients/` and has a timeout plus retry with backoff. Rate limits are real: respect `Retry-After`.
- Handlers must not crash the bot. Catch, log with context, and keep running.
- Log with the `logging` module, not `print`. Never log tokens or user personal data.
- New handlers get a test that mocks the client. No real network calls in tests.

## Don't
- Don't add dependencies without asking. Prefer the standard library.
- Don't change the command names users already rely on: [list them].
- Don't touch `[path]` (generated/vendored).

## Context
- Deployed on: [your PC / Railway / a VPS]. Runs [24/7 / on a schedule].
- Python [3.12+]. Main libraries: [discord.py / python-telegram-bot / httpx / APScheduler].
