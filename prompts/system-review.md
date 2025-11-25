---
description: simplify systems/structures within our codebase
argument-hint: [FOCUS=<focus>]
---

We are looking to drastically simplify systems/structures within our codebase. Detangle, delete, DRY. 

Our target is $1

Use the Oracle tool to perform a comprehensive, deep analysis. You must provide it all the relevant codebase context it needs, though it can browse/research and lookup public docs on it's own.

---

Follow **Elon's 5 Step Engineering Process (***The Algorithm***)**. The order is essential, as doing it out of order leads to a lot of work being done in the wrong direction. A lot in the wrong direction is worse than a little in right direction. Below are the steps with reasoning for why they precede the next step.

1. **Make the requirements less dumb** by questioning every requirement. Challenge my assumptions.
    - Don't build unnecessary things.
2. **The best part/process is no part/process**. If we're not occasionally adding back ~10%, we're not deleting enough. Find things to delete.
    - Don't optimize things that shouldn't exist.
3. **Simplify/optimize** to the essential components, avoiding unnecessary edge-case guards and re-inventing of the wheel.
    - Don't try to accelerate complex things.
4. **Accelerate cycle-time/efficiency** at the current bottleneck. One bottleneck at a time.
    - Don't automate slow processes.
5. **Automate** the most common, simple, arduous, lamentable work.

---

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

Recurring Pain-Points

- not properly leveraging the power of Convex, especially [Convex Components](https://www.convex.dev/components) and `convex-helpers`
- not leveraging popular `npm` libraries, re-inventing the wheel with a bunch of boilerplate (check our existing or find new ones)
- `~/.config/docs/React/ReactEffectsGuide.md`: why useEffects may not be needed