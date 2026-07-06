---
name: repo-onboarding
description: Generate an onboarding cheat-sheet for an unfamiliar repository, covering what it is, the tech stack, architecture, local dev, deployment / CI/CD, databases, and critical engineering points. Produces a single grounded markdown file the user keeps and updates.
when_to_use: Use when the user asks for a "repo summary", "onboarding doc", "overview of this repo", or wants to understand a new codebase as a forward-deployed engineer or new team member.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Repo Onboarding Cheat-Sheet Generator

Produce a grounded, scannable markdown summary of a repository that helps the user (typically a forward-deployed / platform engineer) get productive fast. The output is a personal reference file the user will keep editing — not a polished company doc — unless they say otherwise.

The single most important rule: **NEVER HALLUCINATE.** Every concrete claim (region, registry name, branch name, secret store, env var, service URL, deployment target, sibling repo name) must be traceable to a specific file you read. If you cannot ground it, it goes in the **Open Questions** section, not the body.

## Workflow

### Phase 1 — Confirm path, then proceed

The user has already established durable preferences for this kind of doc — encoded as defaults below. **Do not re-ask things they have already decided.** Only confirm what genuinely varies per repo.

#### Defaults (apply unless overridden)

- **Output location:** `~/Docs/repos-info/<repo-name>.md` as a new markdown file. The user keeps per-repo cheat-sheets in `~/Docs/repos-info/`.
- **Audience and tone:** Personal cheat-sheet — dense, scannable, telegraphic-OK, designed for the user to come back to and update. Not a polished team doc.
- **Scope:** This repo plus ecosystem context **only when grounded** in this repo's files (workflows, values files, env templates explicitly naming sibling repos/services). Never invent ecosystem context.
- **Gaps handling:** Anything that cannot be grounded goes to the **Open Questions** section, listed for the user to fill in by asking the team. Do not skip silently. Do not pause to ask interactively unless the answer would significantly reshape the doc.
- **Length:** No fixed target. Governed by what the repo actually merits — neither padded nor truncated. Skip sections the repo doesn't justify rather than writing thin content.
- **Critical points focus:** Engineering and deployment-relevant footguns, invariants, and non-obvious behaviors. Not generic best-practice advice.

#### What to confirm before reading

Before doing heavy discovery, send a single short message that:

1. States the proposed output path: `~/Docs/repos-info/<repo-name>.md`. Ask only if a different filename is wanted (e.g. the repo name is awkward, or there's already a file there).
2. Asks one targeted question only if there is genuine ambiguity for *this* repo — for example, "should this cover only this repo, or pull in the wider X ecosystem context?" only when there's a real signal that ecosystem context matters.

If nothing genuinely varies, **skip the question round entirely** and proceed to discovery with one sentence stating what you're about to do and where the file will land. The user explicitly does not want to be re-interviewed on things they have already decided.

The defaults above are authoritative for this skill. Do not override them based on memory entries — if the user wants different behavior for a specific run, they will say so in the message that invoked the skill.

### Phase 2 — Discovery (ground every claim)

Walk the repo. Default to read-only tooling (Read, Glob, Grep, `ls`, `git log`) — do not run build/test commands without permission. The goal is to gather *evidence* before writing.

Run discovery in roughly this order, but skip categories that don't apply:

#### 2a. Repo shape

```bash
ls -la                                  # top-level layout
git log --oneline -20                   # what's been moving
git log -1 README.md docs/ 2>/dev/null  # is the docs/README current or stale?
```

Read `README.md` and any `docs/`, but **treat docs as point-in-time snapshots** — verify against code/config before quoting them. If the README references a file or command that no longer exists, that is itself a finding worth noting.

#### 2b. Project type and entry points

Look for whichever of these exist:

| Manifest | Tells you |
|---|---|
| `package.json` | Node project; check `scripts`, `main`, `bin`, dependency names |
| `pyproject.toml` / `setup.py` / `requirements*.txt` | Python; entry points, deps |
| `Cargo.toml` | Rust binary or library; `[[bin]]` is the entry |
| `go.mod` + `cmd/` or `main.go` | Go; what binaries are built |
| `Gemfile` / `pom.xml` / `build.gradle` / `*.csproj` / `mix.exs` | Ruby / Java / .NET / Elixir |
| `Makefile` / `makefile` / `justfile` | Canonical commands the team uses |
| `Procfile` / `app.yaml` / `serverless.yml` | PaaS / serverless deployment |

Identify the **actual entry points** (server, CLI, worker, library) — not what the README claims, what the code does. For services, find the file that boots the HTTP/gRPC server.

#### 2c. Local development

- `docker-compose*.yml`, `devcontainer/`, `.devcontainer/`, `Dockerfile*`
- `Makefile` targets (these are usually the canonical "how to run" commands)
- `.env*` templates — these are gold for understanding configuration surface
- Any `bin/` or `scripts/` directory with operational scripts

Note explicitly if there is no test suite or no linter wired up — that's a finding, not an oversight to gloss over.

#### 2d. Deployment / CI/CD

CI:
- `.github/workflows/*` (GitHub Actions)
- `.gitlab-ci.yml`
- `.circleci/config.yml`
- `Jenkinsfile`
- `azure-pipelines.yml`, `bitbucket-pipelines.yml`

For each workflow, extract: what triggers it (events, branches, paths), what it builds, where it pushes (registry URL, region, repo name), what credentials it uses (OIDC role? long-lived secret?), what it dispatches downstream.

IaC / deploy targets:
- `kubernetes/`, `helm/`, `k8s/` — read `Chart.yaml`, `values*.yaml` carefully; prod values often live in a separate file (`values-ecr.yaml`, `values-prod.yaml`, etc.)
- `terraform/`, `tf/`, `pulumi/`, `cdk/`
- `.argocd/`, Argo Application manifests
- `fleet.yaml`, Rancher Fleet bundles
- `flux/` directories
- Cloud-specific: `app.yaml` (GAE), `serverless.yml`, `sam.yaml`, `cloudbuild.yaml`

Release tooling:
- `release-please-config.json`, `.release-please-manifest.json`
- `.changeset/`, `CHANGELOG.md` and how it's maintained
- `goreleaser.yaml`, `cargo-release.toml`

#### 2e. Data / external systems

- Database: ORM/migration files, schema files, connection-string env vars (`POSTGRES_*`, `DATABASE_URL`, `MONGO_URI`, etc.). Check Helm values for embedded vs. external DB.
- Object storage: S3 / MinIO / GCS / Azure Blob references in code or values files.
- Caches / queues: Redis, RabbitMQ, Kafka, SQS references.
- External APIs and AI providers: gateway URLs, model names, endpoint configurations.
- Secret stores: Infisical (`.infisical.json`), Doppler, Vault, AWS Secrets Manager, SOPS (`.sops.yaml`), 1Password Connect, sealed-secrets.

#### 2f. Observability

- Logging libraries, structured logging conventions
- Tracing (OpenTelemetry, Datadog, MLflow, Sentry) — and importantly, whether calls are wrapped in safe/optional fallbacks
- Metrics (Prometheus annotations in Helm, statsd, etc.)
- Dashboards referenced anywhere

#### 2g. Public surface (libraries) or service contract (services)

- For libraries: the public API surface (`__init__.py` re-exports, `lib.rs` `pub use`, `index.ts` exports). Note what is intentionally exposed vs. internal.
- For services: HTTP/gRPC routes, request/response schemas, version endpoint, health endpoint, any compatibility shims (e.g. emulating another API for clients).

### Phase 3 — Synthesize the doc

Write **one** markdown file at the agreed path. Do not create supporting files unless the user asks.

#### Structural principles

- **Section structure derives from what the repo has, not from a fixed template.** A CLI tool needs no "request path" section; a library needs no "deployment runtime" section; an internal service does need both. Pick sections based on evidence.
- **Lead with TL;DR.** First paragraph should answer "what is this and why does it exist" in plain language, including a one-line note on how/where it deploys if it's a service.
- **Use tables** for tech-stack-at-a-glance, env-var selectors, "what triggers what", "you want to do X → look at Y" file maps. They're scannable and easy to update.
- **Use a single small mermaid flow diagram** for the request path or end-to-end change flow when one exists (apply the mermaid-diagram skill's theming and label rules). Keep it small: a navigational aid, not a replacement for explanation.
- **Critical points / footguns as a numbered list.** This is the section the user re-reads most. Lead each item with the rule, then the *why* (incident, invariant, hidden constraint).
- **End with Open Questions and a File Map.** Open Questions is what makes the doc honest; File Map is what makes it usable next week when the user has forgotten everything.

#### Sections to consider (pick what applies)

- TL;DR — what + why + where it deploys (services only)
- Tech stack at a glance (table)
- Architecture — request path (services), pipeline stages, data model
- Ingest / data flow (data pipelines)
- Public API surface (libraries)
- Configuration & secrets — env vars, config files, secret store, backend selectors
- Local development — how to run, makefile targets, tests/lint status
- CI/CD & deployment — branching, what triggers what, registry/chart paths, hand-off to other repos
- Production runtime — replicas, resources, scheduling, external dependencies (DB, queues, gateways)
- Critical engineering points / footguns — numbered, with *why*
- Mental model of an end-to-end change: one small mermaid flow
- Open questions to verify with the team
- File map — "you want to X, look at Y"

Skip any section the repo doesn't justify. Don't pad with generic advice ("write good tests", "use semantic versioning"). The user already knows.

#### Anti-hallucination rules (hard)

These are non-negotiable. Violating any of them produces a worse-than-useless doc.

1. **Concrete claims must cite evidence.** If you write "AWS region eu-west-2", a workflow file or terraform file must say so. If you write "main branch is `dev`", `.git/HEAD` or actual commits must confirm it.
2. **Do not invent service names, registry paths, env var names, or sibling repo names.** If a sibling repo is named in `.github/workflows/*` or `values*.yaml`, you can mention it. If not, do not.
3. **Distinguish "what the workflow does" from "what the team does".** A README or a teammate's verbal description may diverge from the actual CI config. When they conflict, describe both: state what the code says, then note the divergence as an open question.
4. **Comments in code/config that say "TODO" or "future use" are findings, not promises.** If a workflow has `TARGET_ENV="dev"  # change to prod when ready`, the doc should say "prod is currently not targeted from this repo's automation" — not "deploys to prod".
5. **README/docs may be stale.** Always cross-check before quoting. If stale, note it explicitly so the user knows not to follow the doc blindly later.
6. **Inferences must be labeled.** If you write "this looks like it deploys via Argo CD because of an `Application` manifest", say "looks like" or "likely" — don't assert.
7. **When uncertain, push to Open Questions, not into the body.** It is always better to leave a gap visible than to fill it with a guess.

#### Tone and length

- Personal cheat-sheet → terse, telegraphic, sentence fragments OK, code-shaped tables, dense.
- Shareable team doc → complete sentences, more setup/context, but no padding.
- Length is governed by what the repo actually merits, bounded by what the user said. A simple library does not need a 2000-word document. A multi-service deployment with non-obvious CI does.

### Phase 4 — Hand-off

After writing, output a short summary in chat:

- One sentence on what was produced and where.
- A short bulleted list of the section headings (so the user can mentally index).
- Explicitly call out which open questions are most likely to bite them first (the ones blocking actual work, not nice-to-haves).

Do **not** dump the full document body back into chat — they have the file.

## Things to skip

- Do not generate a README.md or contribute a doc into the repo unless the user explicitly asks. The default output goes to the user's personal notes location.
- Do not commit the file or push anything.
- Do not generate diagrams beyond the single small mermaid flow.
- Do not run tests or builds unless the user has explicitly authorized.

## Memory hooks

If the user has memory configured for this project, after producing the doc consider whether any *durable* facts (sibling repos, deployment patterns shared across the org, secret-store conventions) belong in long-term memory vs. just in the doc. The doc is for *this* repo; memory is for cross-session, cross-repo context. Don't duplicate.
