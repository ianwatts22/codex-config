# AGENTS.md

These are instructions for coding agents. This is our "**global**" AGENTS.md file (`~/.codex/AGENTS.md`). When updating files, make sure to edit the right one (global vs project).

## ESSENTIAL RULES & REMINDERS

- Editing Files: ALWAYS use your built-in `apply_patch` tool, NEVER run `apply_patch` via the shell
- always consult internal (`/docs`) and external (`/.docs-external` or **Context7 MCP**) documentation
- propose updates to global or project `AGENTS.md` instructions to codify best practices
- always search for existing code to maintain SSOT
- use `--help` to better understand CLIs
- fail loud, don't build with bubblewrap for all edge cases
- leverage `morph-mcp`'s warp-grep tool for semantic grep
- when comitting changes from a Linear issue, make sure to find and link the corresponding Github issue
- if told something like "address SYN-10", assume that is a **Linear** issue
- "Oracle" = `oracle` CLI tool (NEVER use `--engine API`)

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

We must keep our codebase `/docs` up to date. Always consult when working on tasks and create docs if they're missing. Resolve or ask for clarification on discrepencies.

Write encompassing yet concise specs as comments at the top of files explaining their purpose, structure, and reasoning. Check before editing files and update as necessary.

### ExecPlans

When writing complex features or significant refactors, use an ExecPlan (as described in `~/.codex/.agent/PLANS.md`) from design to implementation.

---

## Principles

- **best part is no part (***KISS***)**: reduce complexity, focus on what matters
- **single source of truth (***SSOT***)** avoids repetition & inconsistency
  - All business rules, validation, enums, flags, constants, and config live in the Convex backend or `contants.ts`. UI is a pure view that reads them via API or shared types. Do not define duplicate rules or values in the frontend. When the UI needs new options or behavior, change the backend model/config first, then consume it from the UI. If you see frontend code copying backend data or logic, refactor to fetch it from the backend.
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
  - `/components/xyz`: custom/scoped componenets
  - **Registries**: [DiceUI](diceui.com), [Reui](reui.io)
- **Tailwind (v4)**
- **`globals.css`** as SSOT for design tokens (colors, etc.)
- **Lucide** for most icons
- **simple-icons** (`react-icons/si`) for company icons
- **Framer Motion** (`motion/react`)

---

## Testing and Debugging

- keep it simple. Always check our always-on `tmux` sessions (`dev`, `convex`, `build`) or Vercel and Axiom CLIs for logs.
- run `pnpm build` before deploying
- `attach -t` to our `tmux` sessions (`dev`, `convex`, `build`) to debug and check builds
- for **persistent/recurring errors**, inscrubtably investigate where it started failing with the Github and Vercel CLIs to find the root cause

---

## Project Management and Issue Tracking

Ian often does project management in Linear (accessible via `linear` CLI), which syncs with Github, and Notion (sometimes accessible via MCP).

This system is insufficient for complex, real-time agent networks. Therefore, you should use **beads** (`bd`) as explained below. 

### Issue Tracking with `bd` (beads)

**IMPORTANT**: use for ALL issue tracking. Do NOT use markdown TODOs, task lists, or other tracking methods unless told.

#### Why `bd`?

- Dependency-aware: Track blockers and relationships between issues
- Git-friendly: Auto-syncs to JSONL for version control
- Agent-optimized: JSON output, ready work detection, discovered-from links
- Prevents duplicate tracking systems and confusion

#### Quick Start

**Check for ready work:**
```bash
bd ready --json
```

**Create new issues:**
```bash
bd create "Issue title" -t bug|feature|task -p 0-4 --json
bd create "Issue title" -p 1 --deps discovered-from:bd-123 --json
bd create "Subtask" --parent <epic-id> --json  # Hierarchical subtask (gets ID like epic-id.1)
```

**Claim and update:**
```bash
bd update bd-42 --status in_progress --json
bd update bd-42 --priority 1 --json
```

**Complete work:**
```bash
bd close bd-42 --reason "Completed" --json
```

#### Issue Types

- `bug` - Something broken
- `feature` - New functionality
- `task` - Work item (tests, docs, refactoring)
- `epic` - Large feature with subtasks
- `chore` - Maintenance (dependencies, tooling)

#### Priorities

- `0` - Critical (security, data loss, broken builds)
- `1` - High (major features, important bugs)
- `2` - Medium (default, nice-to-have)
- `3` - Low (polish, optimization)
- `4` - Backlog (future ideas)

#### Workflow for AI Agents

1. **Check ready work**: `bd ready` shows unblocked issues
2. **Claim your task**: `bd update <id> --status in_progress`
3. **Work on it**: Implement, test, document
4. **Discover new work?** Create linked issue:
   - `bd create "Found bug" -p 1 --deps discovered-from:<parent-id>`
5. **Complete**: `bd close <id> --reason "Done"`
6. **Commit together**: Always commit the `.beads/issues.jsonl` file together with the code changes so issue state stays in sync with code state

#### Auto-Sync

bd automatically syncs with git:
- Exports to `.beads/issues.jsonl` after changes (5s debounce)
- Imports from JSONL when newer (e.g., after `git pull`)
- No manual export/import needed!

#### Managing AI-Generated Planning Documents

AI assistants often create planning and design documents during development (e.g., PLAN.md, IMPLEMENTATION.md, ARCHITECTURE.md)

**Best Practice: Use a dedicated directory for these ephemeral files**

**Recommended approach:**
- Create a `history/` directory in the project root
- Store ALL AI-generated planning/design docs in `history/`
- Keep the repository root clean and focused on permanent project files
- Only access `history/` when explicitly asked to review past planning

**Benefits:**
- ✅ Clean repository root
- ✅ Clear separation between ephemeral and permanent documentation
- ✅ Easy to exclude from version control if desired
- ✅ Preserves planning history for archeological research
- ✅ Reduces noise when browsing the project

#### CLI Help

Run `bd <command> --help` to see all available flags for any command.
For example: `bd create --help` shows `--parent`, `--deps`, `--assignee`, etc.

#### Important Rules

- ✅ Use bd for ALL task tracking
- ✅ Always use `--json` flag for programmatic use
- ✅ Link discovered work with `discovered-from` dependencies
- ✅ Check `bd ready` before asking "what should I work on?"
- ✅ Store AI planning docs in `history/` directory
- ✅ Run `bd <cmd> --help` to discover available flags
- ❌ Do NOT create markdown TODO lists
- ❌ Do NOT use external issue trackers
- ❌ Do NOT duplicate tracking systems
- ❌ Do NOT clutter repo root with planning documents

#### Using `bv` as an AI sidecar

`bv` is a fast terminal UI for Beads projects (.beads/beads.jsonl). It renders lists/details and precomputes dependency metrics (PageRank, critical path, cycles, etc.) so you instantly see blockers and execution order. For agents, it’s a graph sidecar: instead of parsing JSONL or risking hallucinated traversal, call the robot flags to get deterministic, dependency-aware outputs.

*IMPORTANT: As an agent, you must ONLY use `bv` with the robot flags, otherwise you'll get stuck in the interactive TUI that's intended for human usage only!*

- `bv --robot-help` — shows all AI-facing commands.
- `bv --robot-insights` — JSON graph metrics (PageRank, betweenness, HITS, critical path, cycles) with top-N summaries for quick triage.
- `bv --robot-plan` — JSON execution plan: parallel tracks, items per track, and unblocks lists showing what each item frees up.
- `bv --robot-priority` — JSON priority recommendations with reasoning and confidence.
- `bv --robot-recipes` — list recipes (default, actionable, blocked, etc.); apply via bv --recipe <name> to pre-filter/sort before other flags.
- `bv --robot-diff --diff-since <commit|date>` — JSON diff of issue changes, new/closed items, and cycles introduced/resolved.

Use these commands instead of hand-rolling graph logic; `bv` already computes the hard parts so agents can act safely and quickly.

---

## Tools

The following tools provide help with project management, context/search, and interacting with outside tools. CLI tools are the default/preferred, but you can also access a range of MCP tools through the `mcporter` CLI tool (providing on-demand access to MCPs with a CLI).

### MCPs

The two MCPs you always have access to for intenal docs (`deepwiki`) and external docs (`Context7`).

- `Context7`: doc search for implementing any libraries or APIs to ensure best practice and maximize SOTA paradigms
- `morph-mcp`/`warp-grep`: semantic search/grep across the codebase
- `mcp-agent-mail`: multi-agent coordination (see below)

#### MCP Agent Mail: coordination for multi-agent workflows

**What it is**
- A mail-like layer that lets coding agents coordinate asynchronously via MCP tools and resources.
- Provides identities, inbox/outbox, searchable threads, and advisory file reservations, with human-auditable artifacts in Git.

**Why it's useful**
- Prevents agents from stepping on each other with explicit file reservations (leases) for files/globs.
- Keeps communication out of your token budget by storing messages in a per-project archive.
- Offers quick reads (`resource://inbox/...`, `resource://thread/...`) and macros that bundle common flows.

**How to use effectively**

1) **Same repository**
   - Register an identity: call `ensure_project`, then `register_agent` using this repo's absolute path as `project_key`.
   - Reserve files before you edit: `file_reservation_paths(project_key, agent_name, ["src/**"], ttl_seconds=3600, exclusive=true)` to signal intent and avoid conflict.
   - Communicate with threads: use `send_message(..., thread_id="FEAT-123")`; check inbox with `fetch_inbox` and acknowledge with `acknowledge_message`.
   - Read fast: `resource://inbox/{Agent}?project=<abs-path>&limit=20` or `resource://thread/{id}?project=<abs-path>&include_bodies=true`.
   - Tip: set `AGENT_NAME` in your environment so the pre-commit guard can block commits that conflict with others' active exclusive file reservations.

2) **Across different repos in one project** (e.g., Next.js frontend + FastAPI backend)
   - Option A (single project bus): register both sides under the same `project_key` (shared key/path). Keep reservation patterns specific (e.g., `frontend/**` vs `backend/**`).
   - Option B (separate projects): each repo has its own `project_key`; use `macro_contact_handshake` or `request_contact`/`respond_contact` to link agents, then message directly. Keep a shared `thread_id` (e.g., ticket key) across repos for clean summaries/audits.

**Macros vs granular tools**
- Prefer macros when you want speed or are on a smaller model: `macro_start_session`, `macro_prepare_thread`, `macro_file_reservation_cycle`, `macro_contact_handshake`.
- Use granular tools when you need control: `register_agent`, `file_reservation_paths`, `send_message`, `fetch_inbox`, `acknowledge_message`.

**Common pitfalls**
- "from_agent not registered": always `register_agent` in the correct `project_key` first.
- "FILE_RESERVATION_CONFLICT": adjust patterns, wait for expiry, or use a non-exclusive reservation when appropriate.
- Auth errors: if JWT+JWKS is enabled, include a bearer token with a `kid` that matches server JWKS; static bearer is used only when JWT is disabled.

##### Integrating Agent Mail with Beads

Beads (`bd`) provides dependency-aware issue tracking; Agent Mail handles messaging, audit trail, and file reservations. Use them together.

**Recommended conventions**
- **Single source of truth**: Use **Beads** for task status/priority/dependencies; use **Agent Mail** for conversation, decisions, and attachments (audit).
- **Shared identifiers**: Use the Beads issue id (e.g., `bd-123`) as the Mail `thread_id` and prefix message subjects with `[bd-123]`.
- **Reservations**: When starting a `bd-###` task, call `file_reservation_paths(...)` for the affected paths; include the issue id in the `reason` and release on completion.

**Typical flow (agents)**
1. **Pick ready work** (Beads): `bd ready --json` → choose one item (highest priority, no blockers)
2. **Reserve edit surface** (Mail): `file_reservation_paths(project_key, agent_name, ["src/**"], ttl_seconds=3600, exclusive=true, reason="bd-123")`
3. **Announce start** (Mail): `send_message(..., thread_id="bd-123", subject="[bd-123] Start: <short title>", ack_required=true)`
4. **Work and update**: Reply in-thread with progress and attach artifacts/images; keep discussion in one thread per issue id
5. **Complete and release**:
   - `bd close bd-123 --reason "Completed"` (Beads is status authority)
   - `release_file_reservations(project_key, agent_name, paths=["src/**"])`
   - Final Mail reply: `[bd-123] Completed` with summary and links

**Mapping cheat-sheet**
- Mail `thread_id` ↔ `bd-###`
- Mail subject: `[bd-###] …`
- File reservation `reason`: `bd-###`
- Commit messages (optional): include `bd-###` for traceability

**Pitfalls to avoid**
- Don't create or manage tasks in Mail; treat Beads as the single task queue.
- Always include `bd-###` in message `thread_id` to avoid ID drift across tools.

#### dev-browser (Browser Automation)

Persistent browser automation via Playwright. Use for scraping, form filling, screenshots, testing web UIs, or any browser interaction.

- **Instructions to Run**: `~/.claude/plugins/marketplaces/dev-browser-marketplace/skills/dev-browser/SKILL.md`

#### mcporter

`npx mcporter <server>` is a CLI to run any registered MCP `<server>`. List available servers with `npx mcporter --help`. Common endpoints:

- `shadcn`: interact with items from registries, browse components (w/ docs), and install into project
- `Notion`: general (and code) project management and company knowledge
- `figma`: look at our designs (rarely used)

### CLIs

I've provided some common commands, but use `--help` to fully explore.

#### `oracle`

Oracle queries GPT-5.1 Pro via browser automation. Use when stuck, debugging, or need architectural review.

- Always include `~/.codex/AGENTS.md` and project `AGENTS.md` in `--file` args for context

#### Utilities

- `fd`: simple, fast and user-friendly alternative to "find"
- `rg` (`ripgrep`): improved, modern `grep`
- `jq`: lightweight and flexible command-line JSON processor

#### Exploration

- `scc`: summarize code content
- `git-delta`: syntax-highlighting pager for git and diff output

#### Organization/Management

- `linear`: access our Linear project
  - `i list`: list issues
  - `i view <issue-id>`: view issue
  - `i create`: create issue
- `git`: use **conventional prefiexes** (`feat:`, `fix:`, `refactor:`,  `docs:`, `chore:`, `enhancement:`)
- `github`: all Linear tasks synced with Github issues

#### Debugging

- `sentry`: analyze errors
- `axiom`: analyze and ingest logs
- `vercel`: deploy, inspect, etc.

### Morph MCP `warp_grep` vs `ripgrep`

In addition to `ripgrep`, you have `warp_grep` in `morph-mcp` for semantic search. It does parallel greps, reads relevant sections, follows connections, and returns synthesized context with line numbers instead of whole files.

- **Use for**: unknown files/paths, tracing data flow across files, "how" questions that span 3+ files, findign touch points for cross-cutting concerns, understanding unfamiliar subsystems before modifying
- **DO NOT use for**: quick lookups mid-task, known names/files

---

## Git Guidelines

- link associated **Linear** issues when committing
- Delete unused or obsolete files when your changes make them irrelevant (refactors, feature removals, etc.), and revert files only when the change is yours or explicitly requested. If a git operation leaves you unsure about other agents' in-flight work, stop and coordinate instead of deleting.
- **Before attempting to delete a file to resolve a local type/lint failure, stop and ask the user.** Other agents are often editing adjacent files; deleting their work to silence an error is never acceptable without explicit approval.
- Coordinate with other agents before removing their in-progress edits—don't revert or delete work you didn't author unless everyone agrees.
- ABSOLUTELY NEVER run destructive git operations (e.g., `git reset --hard`, `rm`, `git checkout`/`git restore` to an older commit) unless the user gives an explicit instructions. Treat these commands as catastrophic; if even slightly unsure, stop and ask. *(in Cursor or Codex Web, these git limitations do not apply; use the tooling's capabilities as needed.)*
- Never use `git restore` (or similar commands) to revert files you didn't author—coordinate with other agents instead so their in-progress work stays intact.
- Always double-check git status before any commit
- Keep commits atomic: commit only the files you touched and list each path explicitly. For tracked files run `git commit -m "<scoped message>" -- path/to/file1 path/to/file2`. For brand-new files, use the one-liner `git restore --staged :/ && git add "path/to/file1" "path/to/file2" && git commit -m "<scoped message>" -- path/to/file1 path/to/file2`.
- Quote any git paths containing brackets or parentheses (e.g., `src/app/[candidate]/**`) when staging or committing so the shell does not treat them as globs or subshells.
- Never amend commits unless you have explicit written approval in the task thread.

---

## Simplification Process

- enforce DRY, minimal, readable coding practices
- leverage existing toolkits and find opportunities to expand
- look for opportunities to re-use components throughout the code base
- what dependencies (APIs, libraries, etc.) are we missing that would greatly reduce LOC and improve code readability?

Helpful Tools:

- `scc . --include-ext ts,tsx --by-file`: list files by LOC, complexity, etc. to find the worst offenders
- `knip`: find dead code
- `jscpd`: find duplicated code

---

## Convex Instructions

It is essential to leverage Convex to it's maximum potential.

### CLI

- Preferred: `npx convex run <module>:<export> '<jsonArgs>'`.
  - `<module>` is relative to `convex/` without `.ts` (e.g., `convex/<module>.ts` → `<module>`).
  - DO NOT prefix with `internal/`
- `--prod`: target prod
- `npx convex deploy -y`: deploy

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
- Treat `useMemo` as a performance hint, not a default. Start with plain derived values; only memoize genuinely expensive pure computations or values whose stable identity is required (memoized children, effect deps). Removing `useMemo` should not change behavior, only performance characteristics.
- Default to server components. Add `use client` only when you actually need browser APIs or interactive local state, and keep those client components as thin shells around UI and event handlers.
- Keep React state minimal and canonical. Store the smallest source-of-truth and derive everything else during render; avoid duplicated or “mirrored” state that can drift out of sync.
- Use context only for true cross-cutting concerns (auth, theme, org, feature flags). If a value is only needed in a small subtree, pass it as props instead of introducing a new context.
- Prefer composition over prop-driven branching. Break complex, highly-configurable components into smaller pieces and slot them together instead of accumulating many boolean/variant props.
- Treat `React.memo` and `useCallback` like `useMemo`: opt-in, targeted perf tools. Use them only when you’ve identified a real render hotspot or need stable identities for memoized children/effects.

---

## Auto-Save Pattern

Use `useAutoSave` hook for **save on blur** (no debounced onChange):

```tsx
const { saveOnBlur } = useAutoSave(save, isEditing, hasUnsavedChanges);

<Input
  value={value}
  onChange={(e) => setValue(e.target.value)}
  onBlur={saveOnBlur}
/>
```

- **Search inputs**: use `useDebouncedCallback` at 150ms instead
- **Server**: use `ctx.db.patch` for idempotent updates

See `docs/auto-save.md` for full examples.

---

## Changelog

`content/changelog/*.md` → `/changelog`. Update often after user-visible changes.

Keep it non-technical — users are marketing teams. Only surface what they'd notice or care about.

---
