# AUREN Core Skill — Open Edition

**Skill version:** 1.1.2  
**Core Specs baseline:** 2.4  
**AI Index baseline:** 6.4  
**Owner and author:** Stephan A. Davis  
**Edition:** Open Edition

AUREN Core Open Edition is a portable, open, and auditable Agent Skill for reflective orientation, systemic perspective work, responsibility-preserving decision preparation, AUREN integration, and AUREN Core audits.

Its central commitment is simple:

> AUREN strengthens human judgement. AUREN does not replace human judgement.

## Modes

- **Runtime mode** is the default. It creates a reflective orientation and clarification space.
- **Integration mode** maps the open AUREN Core into another assistant, prompt, workflow, or architecture.
- **Audit mode** reviews a supplied system or interaction design against the open AUREN Core.

Integration and Audit modes require an explicit user request.

## Boundaries

AUREN Core is not a decision authority, therapist, emergency service, clinician, lawyer, financial adviser, or replacement for qualified human support. It is not a copy of the public AUREN CustomGPT, and it does not contain the complete proprietary AUREN, mentoring, leadership, or practitioner methodologies.

## Installation

Install or copy the `auren-core/` directory into an Agent Skills-compatible skills location. The directory name and the `name` field in `SKILL.md` are both `auren-core`.

The core runtime is documentation-based and works offline. Optional remote currentness checks require Python 3.10+ and PyYAML. Full package and release-evidence validation additionally require jsonschema:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/check_remote_sources.py --registry REMOTE-SOURCE-REGISTRY.json --output source-update-report.json
```

Validate the package locally:

```bash
python scripts/validate_package.py .
```

Validate the evaluation inventory and release-evidence record:

```bash
python scripts/validate_release_evidence.py .
python scripts/validate_evals.py .
```

Run all package tests:

```bash
python -m unittest discover -s scripts/tests -v
```

## Open Edition and optional semantic extensions

Version 1.1.0 makes the package boundary explicit: the Open Edition is fully usable on its own, while selected Stephan A. Davis model and framework pages may be used only as optional external semantic context.

The machine-readable catalog is `OPTIONAL-SEMANTIC-REFERENCES.json`; the human-readable policy is `OPTIONAL-SEMANTIC-REFERENCES.md`.

Optional references:

- are not bundled and are not required for core operation;
- do not inherit the package license merely because they are linked;
- cannot override the embedded Core Specs, safety, privacy, or human-responsibility rules;
- are not fetched automatically during ordinary Runtime use;
- may be consulted through host capabilities when explicitly requested or clearly relevant;
- must not be used to reconstruct unpublished or complete proprietary methodology from public traces;
- degrade safely to the Open Core when unavailable.

This gives the public package a clear separation between the open operational Core and optional external depth.

## Evaluation and release evidence

Version 1.1.2 preserves the Open-Edition boundary validation introduced in v1.1.0 and carries forward the v1.0.4 security controls. It also incorporates the three non-blocking assurance improvements identified during independent review:

- URLs containing embedded username/password userinfo are explicitly rejected for direct requests and redirects;
- `SECURITY.md` distinguishes package-internal checksums from the separately published release-ZIP SHA-256 external integrity reference;
- all six structurally distinct update-report classifications used in regression coverage are generated through the production builder and validated against the bundled JSON Schema.

The package validator additionally checks the optional semantic-reference catalog, its edition/version alignment, canonical-host URL constraints, non-bundled status, no-override policy, package-license separation, and required catalog IDs.

The dedicated validator `scripts/validate_release_evidence.py` performs full structural validation. `scripts/validate_evals.py` additionally checks semantic relationships, manifest-derived version alignment, case uniqueness, mode parity, high-risk language parity, trigger coverage, and non-claim discipline. Package validation also cross-checks artifact-sensitive evidence fields, including `SKILL.md` line count and release-evidence timestamp ordering (`generated_at` must not precede any recorded run).

The evaluation files are synthetic. Static package validation, JSON-Schema validation, inventory validation, unit tests, and checksum verification can be executed locally. Behavioral model or host results must be recorded only after they are actually run; the included evidence record does not claim unperformed host testing.

See:

- `evals/evals.json`
- `evals/description-trigger-evals.json`
- `evals/release-evidence.schema.json`
- `evals/release-evidence-v1.1.2.json`
- `references/update-report.schema.json`
- `evals/RELEASE-EVIDENCE.md`

## Source hierarchy

1. `references/auren-core-specs_v2.4.yaml`
2. `references/auren-core-logic_v2.4.md`
3. `references/README_v2.4.md`
4. `references/Guidance4AIsystems_v2.4.txt`
5. external AI Index as supplementary semantic context only
6. optional semantic references from `OPTIONAL-SEMANTIC-REFERENCES.json` as non-operational external context only

The embedded YAML remains the operational source of truth.

## Remote currentness

The **remote currentness registry** covers only version/update detection for approved Core sources:

- `ai-index.txt`
- `README_v2.4.md`
- `auren-core-logic_v2.4.md`
- `auren-core-specs_v2.4.yaml`
- `auren-core-specs_v2.4.yaml.txt`
- `Guidance4AIsystems_v2.4.txt`

The checker detects changes and produces a recommendation. It does not self-update the skill. Security invariants are enforced in code and mirrored exactly in the registry as documentation; the registry cannot expand the host allowlist without failing validation. Operational changes require human approval, regression tests, and a new release.

## Privacy

No user content is sent to the update endpoints. Ordinary reflective use never triggers a remote check. The skill requests only task-relevant context and never claims confidentiality or storage guarantees beyond the host platform's documented behavior.

See `PRIVACY-AND-DATA-MINIMIZATION.md`.

## Licensing

This is a mixed-license Open Edition package:

- content, documentation, reference texts, examples, and content evals: **CC BY-SA 4.0**;
- Python scripts and test code: **MIT License**;
- the AUREN name, official edition identity, optional linked proprietary models, and external resources: separately reserved or governed by their own terms.

Optional semantic references are links/context pointers only. Their content is not relicensed by this package.

See `LICENSE`, `LICENSES/`, `ATTRIBUTION.md`, `SOURCE-MATERIAL-NOTICES.md`, and `BRAND-AND-NAME-NOTICE.md`.

## Package map

```text
auren-core/
├── SKILL.md
├── README.md
├── GOVERNANCE.md
├── PRIVACY-AND-DATA-MINIMIZATION.md
├── SECURITY.md
├── ATTRIBUTION.md
├── BRAND-AND-NAME-NOTICE.md
├── SOURCE-MATERIAL-NOTICES.md
├── RIGHTS-LICENSE-EDITION-MATRIX.md
├── RIGHTS-LICENSE-EDITION-MATRIX.json
├── REMOTE-SOURCE-REGISTRY.json
├── OPTIONAL-SEMANTIC-REFERENCES.json
├── OPTIONAL-SEMANTIC-REFERENCES.md
├── REMOTE-SOURCE-UPDATE-CHECK.md
├── EMBEDDED-REFERENCES.json
├── RELEASE-MANIFEST.json
├── CHECKSUMS.sha256
├── CHANGELOG.md
├── LICENSE
├── LICENSES/
├── references/
├── evals/
│   ├── evals.json
│   ├── description-trigger-evals.json
│   ├── release-evidence.schema.json
│   ├── release-evidence-v1.1.2.json
│   └── RELEASE-EVIDENCE.md
├── examples/
└── scripts/
```
