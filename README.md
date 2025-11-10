# .codex settings repo

This repository tracks the Codex agent configuration that lives in `~/.codex` so Ian can version changes to prompts, agent rules, and tooling preferences.

## Contents
- `AGENTS.md`: global agent operating rules.
- `config.toml`: CLI + runtime defaults.
- `prompts/`: saved reusable prompt templates.
- `version.json`: Codex CLI version metadata.

Runtime artifacts (auth tokens, logs, per-session archives) are intentionally ignored via `.gitignore` so secrets stay out of version control.
