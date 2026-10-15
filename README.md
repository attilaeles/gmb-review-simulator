# Synthetic customer review workflow

A client-configurable workflow specification for creating labelled synthetic customer-review datasets for internal testing, workflow demonstrations and reporting development.

The design separates structured visit simulation—customer personas, experiences, outcomes and scores—from LLM-generated review wording. Reviews are fictional and must not be published as genuine customer testimonials.

## Current status

This repository contains the workflow plan, JSON Schema contracts, agent instructions and a specification-validation script. It is a project scaffold, not a runnable review generator.

The generation pipeline, provider integration, runtime configuration loading, automatic quality checks, checkpoint execution and exports still need implementation. The checks described below are requirements for that implementation. Manifest and quality-report schemas also remain future work.

## Intended workflow

1. **Intake:** select a client, read its external knowledge base and collect the request brief and store list. Extract volume, reporting dates and language targets from supplied documents; ask for missing or ambiguous values.
2. **Archive validated inputs:** move request files into `projects/<project_id>/source_inputs/<intake_id>/`, preserving originals and verifying hashes before removing inbox copies. Record a transfer manifest and update source references. Incomplete or ambiguous requests stay in `inputs/`.
3. **Step 0 — Create personas:** define customer goals, expectations, review behaviour and writing styles; validate coverage and sampling weights.
4. **Recommend scenarios:** prepare compatible positive, mixed and negative experiences, including outcome constraints. Obtain explicit approval of the exact scenario-library version before simulation.
5. **Configure and simulate:** set dates, languages, sampling rules, volume and budget; simulate visits, outcomes, ratings and recommendation scores.
6. **Select and write reviews:** decide probabilistically which visits produce reviews, then use an LLM to generate text from their canonical facts.
7. **Validate and save:** check language, length, factual consistency and duplication; retry within limits and retain failures. Save structured records and reporting exports.
8. **Report quality:** summarize counts, distributions, failures, spending and any unmet targets.

Every major stage requires a durable quality checkpoint. Scenario approval is the mandatory human approval gate; other checkpoints are designed as automatic quality gates. Failed checks block dependent work while preserving recovery details. Runtime controls include bounded retries, spending limits, pause/resume and duplicate-safe persistence.

See [the workflow plan](planning/workflow_plan.json) for the complete process and [AGENTS.md](AGENTS.md) for agent operating instructions.

## Local setup

Use Python 3 and run these commands from the repository root. The activation command below is for macOS/Linux shells.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
mkdir -p inputs projects
```

For a new checkout, copy the configuration template to `.env`. Keep an existing `.env` if already configured.

```sh
cp .env.example .env
```

Edit `.env` to point to your external client knowledge base:

```dotenv
CLIENT_KB_ROOT="/absolute/path/to/client-knowledge-base"
```

This is a configuration template: the current scaffold does not automatically load `.env`. Supply the configured path to the agent during preparation; the future pipeline must implement loading it. The sibling KB path mentioned in the agent instructions and plan is the original workspace convention; use the explicit root override for your installation.

The expected knowledge base has a root client index and separate client folders with their own indexes. Relevant records describe the business, markets, products or services, positioning, customer expectations and stores. Read any KB instructions and open questions, retain source provenance, and keep clients separate. Supply missing store records or briefs through `inputs/`. The external KB is read-only for this workflow and is not included in this repository.

No LLM credentials are needed to validate the specifications. Provider configuration will be required when generation is implemented.

## Project structure

```text
AGENTS.md                         Agent operating instructions
README.md                         Project introduction and setup
.env.example                      Generic local configuration template
requirements-dev.txt              Specification-validation dependency
planning/
  workflow_plan.json              Workflow, controls and quality gates
  synthetic_reviews.schema.json  Project and record contracts
  checkpoint.schema.json         Stage checkpoint contract
scripts/
  validate_planning.py           Specification checks
inputs/                           Local request inbox; created during setup
projects/
  .gitkeep                        Tracks the otherwise empty directory
  <project_id>/                   Local project data
    source_inputs/<intake_id>/    Archived request files and transfer manifest
    checkpoints/                  Preparation checkpoints
    runs/<run_id>/                Run records, checkpoints and exports
```

The assembled project schema describes a complete configuration. Draft intake and libraries remain preparation artifacts until required fields are resolved. Schema versions identify contracts; artifact versions identify revisions. Output JSON is required to include descriptive `commit_text` and change history, without requiring an actual Git commit.

## Planned outputs and data handling

- **JSON:** project configuration, personas, scenarios, approval records, manifests, checkpoints and quality reports.
- **JSONL:** simulated events, accepted reviews and generation attempts, linked by stable IDs.
- **CSV:** a derived reporting view with date, store ID, store address, rating, recommendation and review text.
- **Quality report:** accepted and failed counts, distributions, checks, estimated cost and completion or partial-run status.

Client briefs, archived originals, store records and generated project data stay local. `.gitignore` excludes `inputs/`, `session_history/`, `.env` files and everything in `projects/` except `.gitkeep`. The external knowledge base is outside this repository. Local historical material is not needed to use the published scaffold.

Ignore rules do not remove files already tracked or previously committed. Review staged files before pushing, and keep credentials and business information out of shared specifications and examples. Preserve synthetic-data labels in canonical records and downstream reports.

## Limitations

- **Limited store-level differentiation:** With equal store sampling and shared experience/scoring rules, review counts should be approximately even and average ratings and recommendation scores should be similar, with random variation. The baseline design does not model meaningful store-performance differences and should not be used to rank stores. Equal counts or identical means are not guaranteed; explicit store weights or eligibility differences can change distributions.
- **Modelled assumptions:** Persona weights, incident frequencies and review-writing probabilities are simulation inputs, not measured customer behaviour. Review selection can change the mix of reviews relative to the mix of visits.
- **Synthetic recommendation scores:** Recommendation values are generated from the configured model and are not measured customer NPS.
- **Generation variability:** A fixed seed can reproduce structured simulation when code and configuration are fixed; LLM wording may still vary. Semantic quality checks are fallible and should be assessed in a pilot.
- **Implementation pending:** The repository currently validates specifications, not generated review quality or an end-to-end provider integration.

## Validate specifications

After installing the development dependency, run:

```sh
python scripts/validate_planning.py
```

This checks planning JSON syntax, JSON Schema definitions, external schema references and checkpoint declarations for all major stages. It does not execute the workflow or validate actual client data, generated reviews or downstream reporting integrations.
