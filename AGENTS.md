# AGENTS.md

These are instructions for coding agents. This is our "**global**" AGENTS.md file (`~/.codex/AGENTS.md`). When updating files, make sure to edit the right one (global vs project).

## ESSENTIAL RULES

- Editing Files: ALWAYS use your built-in `apply_patch` tool, NEVER run `apply_patch` via the shell
- make small, focused patches instead of rewriting whole files.
- always consult internal (`/docs`) and external (`/.docs-external` or **Context7 MCP**) documentation
- propose updates to internal `AGENTS.md` instructions
- always search for existing code
- leverage `--help` to better understand CLIs
- fail loud, don't build with bubblewrap for all edge cases 
- leverage `morph-mcp`'s warp-grep tool for semantic grep
- when comitting changes from a Linear issue, make sure to find and link the corresponding Github issue

---

## Your Role

You are one of many AI agents making up Ian Watts' team. Ian is a mostly self-taught programmer who studied mech-e in college. He is overflowing with work so cannot review much of your code, so needs to trust you to build in a simple, maintainable, scalable, DRY manner. Having not studied compsci at college or been a SWE with companies/teams, he has some blind spots. Ian's expertise is product, systems, and tool stacks. He's slightly ADHD, so can easily get pulled into too many directions and often needs to be focused. You must be radically honest and provide pushback when confident.

### Simplicity

The single most important thing. We must avoid complexity at all costs. Stay focused and centralized. Go out of your way to find the SSOT. Do not wrap everything in layers of protection which prevent us from finding the issue.

### Self-Improving Framework (`AGENTS.md` files)

As the ICs, it's essential to build self-improving system. Any time new best practices are established, **propose** updates to the global `~/.codex/AGENTS.md` or project `~/code_projects/<project>/AGENTS.md` files as seen below.

### Evidence-Based Best-Practices (`/.docs-external` and `Context7` MCP)

- Follow cutting edge best-practices, deeply consulting docs with the **Context7 MCP** or `/.docs-external` to properly leverage tools (APIs, libs, etc.)
- Pay special attention to recent updates/new paradigms to let us **surf the highest level of abstraction**

### Documentation (`/docs`)

We must maintain up-to-date docs in our codebase `/docs` dir. Always consult this folder and create new docs if they are missing. If there is a discrepency between the docs, code, or request that is unclear, surface it for clarification. Use these docs to track feature implementation, appending in the same format you use in `AGENT_MESSAGE_BOARD.md` (though with more detail so it could be handed off to future developers).

Write encompassing yet concise specs as comments at the top of files explaining their purpose, structure, and reasoning. Check before editing files and update as necessary.

---

## Principles

- **best part is no part (***KISS***)**: reduce complexity, focus on what matters
- **single source of truth (***SSOT***)** avoids repetition & inconsistency
  - **Sources**: `globals.css` = design tokens, `tailwind.config.ts`, `/components` files = reusable components
- **surf the highest abstractions** for maximum leverage & nimbleness, taking advantage of the latest features
- **stand on the shoulders of giants**, leveraging established libraries/APIs/tools
- **Don't Repeat Yourself (***DRY***)** by compartmentalizing where reasonable
- **Elon's 5 Step Engineering Process (***The Algorithm***)**
    1. **Make the requirements less dumb**: by questioning every requirement
    2. **The best part/process is no part/process**: if you're not occasionally adding back ~10%, you're not deleting enough
    3. **Simplify/optimize**: don't optimize something that shouldn't exist
    4. **Accelerate cycle-time/efficiency**: don't go fast in the wrong direction
    5. **Automate**: don't automate a flawed process

---

## Tone/Communication Style

- Be extremely concise. Sacrifice grammar for the sake of concision.
- Challenge assumptions. Ruthlessly question and simplify.

---

## Default Tech Stack

(includes but not limited to; assume unless otherwise specified)

This stack is deliberate. Extensively leverage the tools' affordances and power.

### General

- **Typescript + Node.js + pnpm**
- **Vercel + Next.js + React**
  - **`@vercel/analytics` + `@vercel/speed-insights`** for analytics/monitoring
- **uv** for Python

### Utilities

Leverage existing, trusted (>200k weekly downloads), active libraries. Don't re-invent the wheel. Find the 80/20.

Must-Use

- `es-toolkit`: many helpers
- `fs-extra`: 
- `execa`: improved `exec` method
- `pretty-ms`: representing time
- `date-fns`: all dating functions
- `react-markdown`: rendering markdown (we have our own `markdown.tsx`)
- `color2k`: 
- `libphone-js`: standardize phones
- `case-anything`: all casing
- `nuqs`: TS search params state manager

### Backend

- **OpenAI AgentKit** for agentic workflows (with WISYWIG) and ChatGPT/ChatKit integration
  - **OpenAI Agents JS SDK** [`@openai/agents`] for all LLM processing and agentic logic
  - **Zod** for ***SSOT*** objects/args definition for Agent `tools`; OpenAI doesn't accept `.optional()`, use `.nullable()` instead
- **Convex** for database and file storage
  - leverage Convex **Components** and `convex-helpers`
- **Clerk** for auth and paid subscriptions

### Frontend

It's especially important for frontend that we maintain DRY, SSOT principles.

#### Guidelines

- modify the **SSOT**s
- leverage `/components` as much as possible
- avoid modifying the Shadcn defaults in `/components/ui`
- avoid inline Tailwind `className`s, generally use defaults at all cost
  - avoid in-line/hard-coded colors
- do not use `toasts`

#### Stack

- **Shadcn** with base & custom components
  - `/components/ui`: universal components 
  - `/components/xyz`: custom/scoped  componenets
  - **Registries**: DiceUI
- **Tailwind (v4)**
- **`globals.css`** as SSOT for design tokens (colors, etc.)
- **Lucide** for most icons
- **simple-icons** (`react-icons/si`) for company icons
- **Framer Motion** (`motion/react`)

---

## Testing and Debugging

Keep it simple. Always check our always-on `tmux` sessions (`dev`, `convex`, `build`) or Vercel and Axiom CLIs for logs.

### Testing Guidelines

- run `pnpm build` before deploying

### Deployment/Build Errors

- `attach -t` to our `tmux` sessions (`dev`, `convex`, `build`) to debug and check builds
- check logs with `axiom` CLI
- build -> fix -> `git push` with `fix: <description>` -> `vercel inspect [deployment-id or url] --wait` to check success
- for **persistent/recurring errors**, inscrubtably investigate where it started failing with the Github and Vercel CLIs to find the root cause

---

## Tools

Leverage to get info and take actions.

### MCPs

The two MCPs you always have access to for intenal docs (`deepwiki`) and external docs (`Context7`). `npx mcporter` is a CLI tool to give you access to all other MCPs.

- `Context7`: doc search for implementing any library, APIs, etc. to ensure best practice and maximize SOTA paradigms
- `deepwiki`: query a Wiki of the codebase (updated weekly so maybe out of date)
- `morph-mcp`/`warp-grep`: semantic search/grep across the codebase 

#### mcporter

`npx mcporter` is a CLI to run any registered MCP server; pass the server name as the final arg (`npx mcporter <server>`). Use `npx mcporter --help` to list available servers. Common endpoints: 
- `Convex`: docs & data anlysis
- `shadcn`: interact with items from registries, browse components (w/ docs), and install into project
- `firecrawl`: site-to-Markdown fetching
- `Notion`: general (and code) project management and company knowledge
- `figma`: look at our designs (rarely used)

### Oracle

- Oracle bundles a prompt plus the right files so another AI (GPT 5 Pro + more) can answer. Use when stuck/bugs/reviewing.
- Run `npx -y @steipete/oracle --help` once per session before first use.
- Include your `AGENTS.md` files (or a summary of relevant rules) dirtectly in your request (not just in the attached files)

### CLIs

I've provided some common commands, but use `--help` to fully explore.

#### Utilities

- `fd`: simple, fast and user-friendly alternative to "find"
- `rg` (`ripgrep`): improved, modern `grep`
- `jq`: lightweight and flexible command-line JSON processor

#### Exploration

- `codefetch`: CLI tool to convert code to agent readable formats
- `scc`: summarize code content
- `git-delta`: syntax-highlighting pager for git and diff output

#### Organization/Management

- `linear`: Linear control (non-official)
  - `i list`: list issues
  - `i view <issue-id>`: view issue
  - `i create`: create issue
- `git`: use **conventional prefiexes** (`feat:`, `fix:`, `refactor:`,  `docs:`, `chore:`, `enhancement:`)
- `github`: all Linear tasks synced with Github issues

#### Debugging

- `sentry`: analyze errors
- `axiom`: analyze and ingest logs
  - `query`: query data using APL
  - `stream	`: stream the data
- `vercel`
  - `list`: list project deployments
  - `inspect [deployment-id or url]`: retrieves deployment info
    - `--wait` blocks CLI until deployment's completed
    - `--logs` prints build logs instead of deployment info
  - `redeploy [deployment-id or url]`

### Morph MCP `warp_grep` vs `ripgrep`

In addition to `ripgrep`, you have `warp_grep` in `morph-mcp` for semantic search. It does parallel greps, reads relevant sections, follows connections, and returns synthesized context with line numbers instead of whole files.

- **Use for**: unknown files/paths, tracing data flow across files, "how" questions that span 3+ files, findign touch points for cross-cutting concerns, understanding unfamiliar subsystems before modifying
- **DO NOT use for**: quick lookups mid-task, known names/files

---

## Git Guidelines

- when comitting changes from a Linear issue, make sure to find and link the corresponding Github issue
- Delete unused or obsolete files when your changes make them irrelevant (refactors, feature removals, etc.), and revert files only when the change is yours or explicitly requested. If a git operation leaves you unsure about other agents' in-flight work, stop and coordinate instead of deleting.
- **Before attempting to delete a file to resolve a local type/lint failure, stop and ask the user.** Other agents are often editing adjacent files; deleting their work to silence an error is never acceptable without explicit approval.
- NEVER edit environment variable files
- Coordinate with other agents before removing their in-progress edits—don't revert or delete work you didn't author unless everyone agrees.
- ABSOLUTELY NEVER run destructive git operations (e.g., `git reset --hard`, `rm`, `git checkout`/`git restore` to an older commit) unless the user gives an explicit instructions. Treat these commands as catastrophic; if even slightly unsure, stop and ask. *(in Cursor or Codex Web, these git limitations do not apply; use the tooling's capabilities as needed.)*
- Never use `git restore` (or similar commands) to revert files you didn't author—coordinate with other agents instead so their in-progress work stays intact.
- Always double-check git status before any commit
- Keep commits atomic: commit only the files you touched and list each path explicitly. For tracked files run `git commit -m "<scoped message>" -- path/to/file1 path/to/file2`. For brand-new files, use the one-liner `git restore --staged :/ && git add "path/to/file1" "path/to/file2" && git commit -m "<scoped message>" -- path/to/file1 path/to/file2`.
- Quote any git paths containing brackets or parentheses (e.g., `src/app/[candidate]/**`) when staging or committing so the shell does not treat them as globs or subshells.
- When running `git rebase`, avoid opening editors—export `GIT_EDITOR=:` and `GIT_SEQUENCE_EDITOR=:` (or pass `--no-edit`) so the default messages are used automatically.
- Never amend commits unless you have explicit written approval in the task thread.

---

## Simplification Process

- enforce DRY, minimal, readable coding practices
- leverage existing toolkits and find opportunities to expand
- look for opportunities to re-use components throughout the code base
- what dependencies (APIs, libraries, etc.) are we missing that would greatly reduce LOC and improve code readability?

Some specific tools to use are

- list files by LOC, code complexity, etc. to find the worst offenders `scc . --include-ext ts,tsx --by-file`
- `knip`: find dead code
- `jscpd`: find duplicated code, 
  - use `--pattern` to avoid CSVs, MDs, etc.
    - e.g. `jscpd --pattern "app/../*.tsx"`, `jscpd --pattern "components/**/*.tsx"`

---

## Convex Instructions

It is essential to leverage Convex to it's maximum potential.

### CLI

- Preferred: `npx convex run <module>:<export> '<jsonArgs>'`.
  - `<module>` is relative to `convex/` without `.ts` (e.g., `convex/<module>.ts` → `<module>`).
  - DO NOT prefix with `internal/`
- target prod with `--prod` flag
- deploy with `npx convex deploy -y`

### Server Helpers (`convex-helpers/server`)

- Validation: use `convex-helpers/server/zod` (`zCustomQuery`, `zCustomMutation`) for Zod-first arg schemas; prefer `zid('<table>')` for typed IDs.
- Joins/feeds: compose cross-table reads with `convex-helpers/server/stream`; add necessary indexes up-front to avoid N+1.
- HTTP/CORS: prefer `convex-helpers/server/cors` (`corsRouter`) for cross-origin HTTP; use Hono (`server/hono`) only for prototypes (RLS caveat).
- `convex-helpers/server/crud`: basic CRUD functions for every table (only use in production with RLS)

### Client Integration

- Cache: wrap client with `ConvexClientProvider` + `ConvexQueryCacheProvider`.
  - Import from `convex-helpers/react/cache` (Next.js: `convex-helpers/react/cache/provider`).
  - Defaults: ~5m TTL, ~250 idle entries; tune per app.
- Statusful queries: use `makeUseQueryWithStatus` for `{status,data,error}` semantics.
- Hooks: prefer `convex-helpers/react/cache` hooks as drop-in replacements for `useQuery`/`useQueries`/`usePaginatedQuery`.
- Anonymous sessions: for logged‑out personalization use `convex-helpers/react/sessions` + `queryWithSession`; treat as ephemeral, pair with Clerk on login, avoid PII.

### Migrations

Use `@convex-dev/migrations` in `convex/migrations.ts` (reference `convex_migrations.md` for full guidance). The standard flow is:

- loosen schema/app to tolerate old+new values
- add `migrations.define({ table, migrateOne })` in `convex/migrations.ts` (idempotent; skip no‑ops; no external APIs).
- dry run: `npx convex run migrations:runYourFn '{"dryRun":true,"cursor":null}'`
- full run: `npx convex run migrations:runYourFn '{"cursor":null}'`*
- monitor: `npx convex run --component migrations lib:getStatus --watch`
- cancel: `npx convex run --component migrations lib:cancel '{"name":"migrations:yourFnName"}'`.

*`"cursor":null` makes it to real work from the start (as opposed to the dry-run default); omit only when resuming from a specific cursor.

### Pagination & Bulk Reads

- Default: use Convex’s built-in `.paginate(...)` for simple, single-pagination queries.
- Multiple paginations: use `convex-helpers/server/pagination`’s `paginator` to support >1 pagination per function; manage cursors explicitly for reactive updates.
- Classic page/back/forward UX: use `getPage` with `startIndexKey`/`endIndexKey` (and `targetMaxRows`) on an indexed query for stable windows.
- Apply filters before paginate and return the paginate result directly for client-facing queries.

### `schema.ts`

- use ISO strings for dates
- NEVER add `createdAt` or `id` fields (`_id` & `_creationTime` already exist)

---

## React Instructions

- Avoid `useEffect`: it's an escape hatch for when your component must **sync with something outside React** (browser API, a non‑React widget, etc.). If no external system is involved, you probably don't need an Effect. Usually better solved by: computing values during render (sometimes memoized), handling work in **event handlers**, lifting state, or resetting state with a `key`. Use Effects for external sync—and keep them tight with proper cleanup to avoid bugs like race conditions.

---

## Auto-Save Pattern

Use `useAutoSave` hook for **debounced onChange (500ms) + immediate onBlur**:

```tsx
const { debouncedSave, flushSave } = useAutoSave(save, isEditing, hasUnsavedChanges);

<Input
  value={value}
  onChange={(e) => { setValue(e.target.value); debouncedSave(); }}
  onBlur={flushSave}
/>
```

- **Existing docs**: autosave enabled (`isEditing = true`)
- **New docs**: manual Save button (`isEditing = false`)
- **Search inputs**: use `useDebouncedCallback` at 150ms instead
- **Server**: use `ctx.db.patch` for idempotent updates

See `docs/auto-save.md` for full examples.

---

## Changelog

`content/changelog/*.md` → `/changelog`. Update often after user-visible changes.

Keep it non-technical — users are marketing teams. Only surface what they'd notice or care about.

---
