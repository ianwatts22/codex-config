Our code should be as simple as possible.

- enforce DRY, minimal, readable coding practices
- leverage existing toolkits and find opportunities to expand
- look for opportunities to re-use components throughout the code base
- what dependencies (APIs, libraries, etc.) are we missing that would greatly reduce LOC and improve code readability?

Specific CLIs/commands to help:

- `scc . --include-ext ts,tsx --by-file`: list files by LOC, code complexity, etc. to find the worst offenders 
- `codefetch`: convert code into markdown
- `knip`: find dead code
- `jscpd`: find duplicated code, 
  - use `--pattern` to avoid CSVs, MDs, etc.
    - e.g. `jscpd --pattern "app/../*.tsx"`, `jscpd --pattern "components/**/*.tsx"`

Some specific pain-points or documentation

- `~/.config/docs/React/ReactEffectsGuide.md`: why useEffects may not be needed