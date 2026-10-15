# Synthetic review project

## Purpose and authority

Generate explicitly synthetic customer-review datasets for internal testing and reporting demonstrations. Follow the user's current instructions, then this file and the versioned workflow in `planning/workflow_plan.json`. The project is currently a specification and scaffold; the archived reference Python is not a production generator.

Start by reading `README.md`, `planning/workflow_plan.json` and the relevant schemas. Keep `session_history/` unchanged as historical evidence. Do not import its example client, store count, dates, weights or unresolved modelling choices as current defaults.

## Client intake

Use the external `../mktg_kb_clients` knowledge base read-only, with an explicit root override if relocated. Read its `AGENTS.md` and root `index.md`, resolve the explicitly selected client, then read the client index and relevant overview, open questions, strategy, product and store pages. Never mix clients. Ask for client identity if missing or ambiguous.

Extract the client description and store list with source paths, hashes, retrieval time and evidence status. Surface material conflicts and unknowns. Explicit user corrections take precedence and must retain provenance. Do not update the KB as a side effect of generation.

Extract targets from initial documents before asking. Prompt only for missing or ambiguous volume mode (visits or accepted reviews), count, reporting dates and languages/mix. Do not invent these targets. Preparation that does not depend on targets may proceed while they are pending. Resolve provider and spending limits before paid calls, including setup and QA calls.

After ownership, required fields and targets are resolved and intake validation succeeds, move the request files from `inputs/` into `projects/<project_id>/source_inputs/<intake_id>/`. This is a required part of intake, without a separate permission request. Inventory original paths, sizes and hashes in a versioned `intake_manifest.json`; preserve filenames, subfolders and original bytes in a unique intake directory. Copy and verify each destination before removing its unchanged inbox original. Never overwrite archived originals or transfer unrelated requests. Update source references, record completion and finalize the passed intake checkpoint only after the transfer is verified. Remove empty request folders, preserving the inbox and housekeeping files.

Incomplete, ambiguous, unreadable or validation-failed requests stay in the inbox with blockers recorded. If transfer fails, retain its manifest and verified copies, keep unverified originals, and resume using hashes and recorded transfer status. Later additions use a new intake ID and invalidate affected downstream checkpoints. The external KB remains in place and read-only.

## Workflow and quality checkpoints

Follow intake and steps 0–8 in the plan: personas; scenario recommendations; configuration; visit simulation; review selection; text generation; review validation; persistence/export; quality report/handoff.

Save a durable checkpoint after every major stage using `planning/checkpoint.schema.json`. A checkpoint records artifact paths, versions and hashes, checks and results, blockers, next action and approval evidence where required. Failed or pending stages do not release dependent work. Other independent preparation may continue.

Persona setup has an automatic quality checkpoint for relevance, distinct voices, coverage and valid probabilities. Do not add a human approval requirement unless the user requests it.

Scenario creation has a mandatory human approval gate: present the concrete recommended library, weights, coverage, eligibility and outcomes; save a pending checkpoint; wait for explicit approval of that exact version/hash before simulation. Record the actual approval without inventing an identity or timestamp. Any scenario content, weight, eligibility or outcome change requires fresh approval.

All other checkpoints are automatic quality gates, not permission requests. Stages 3–6 may run in batches, each with linked checkpoints; also persist each event and attempt. Store preparation checkpoints under `projects/<project_id>/checkpoints/` and run checkpoints under `projects/<project_id>/runs/<run_id>/checkpoints/`.

Resume only after verifying dependency and artifact hashes. Invalidate affected downstream checkpoints when inputs change, retaining earlier records. Preserve valid independent work. Never overwrite completed run snapshots. A final checkpoint may validate a truthful partial-run report without declaring the target complete.

## Simulation and review constraints

Keep scenario templates free of fixed visit dates, store IDs and final ratings. Select only compatible persona, scenario, store, date, language, category and channel combinations. No-incident events require severity `none` and resolution `not_applicable`; incident events require an allowed actual severity/resolution pair. Do not sample these independently. Reject contradictory canonical facts before prompting.

Structured simulation owns scores and facts. The LLM writes review text only. Generate text only for selected events. Validate schema, language, configured length, factual/outcome consistency, prompt artifacts and duplicates. Retain failed attempts and bounded retry reasons. Uncertain candidates remain pending and do not count as accepted reviews. Check run distributions, selection bias, references, export row counts and read-back before handoff.

## Operational controls

Apply the plan's preflight, budgets, request limits, timeouts, backoff, retry caps, circuit breaker and pause/resume rules. Count preparation, generation, validation and retries against spending limits. Restore usage and reservations when resuming. Keep secrets outside saved artifacts.

Use stable IDs and idempotent acceptance. Persist events, attempts, budget counters and resumable state before marking completion. Write checkpoints atomically; stop dependent dispatch on persistence failure. On cancellation or budget exhaustion preserve output and report an accurate partial/cancelled state and stop reason.

## Versioning and output

Use JSON for configurations, libraries, manifests, approvals, checkpoints and reports; JSONL for event/review/attempt collections. CSV is a derived reporting export. Every JSON output needs a schema version and artifact version, meaningful `commit_text`, and append-only change history. JSONL rows carry schema/artifact versions and reference a manifest with change metadata. JSON Schema documents use `$schema` and `x-artifact-metadata` for their own contract and revision metadata.

A commit text explains what changed and why; it does not require a Git commit. Never invent a Git hash or historical timestamp. Increment artifact versions on edits and schema versions only when contracts change. Record source, library, prompt/model and configuration lineage. Preserve explicit synthetic labels in canonical output and reporting manifests/dashboard context.

## Project hygiene and verification

Keep pending request materials in `inputs/` and archive validated originals under the project’s `source_inputs/`; keep project-specific artifacts in `projects/<project_id>/`, shared specifications in `planning/`, and helpers in `scripts/`. Do not create pretend client data or successful checkpoints to fill the scaffold.

Run `python3 scripts/validate_planning.py` after changes to planning JSON/schemas. This checks syntax, schema definitions and stage checkpoint coverage; it does not prove a generator or provider integration works. Apply cross-record and semantic checks during implementation. Report what was actually validated and remaining limitations.
