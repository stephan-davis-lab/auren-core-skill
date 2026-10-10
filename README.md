# AUREN Core Skill — Open Edition

**Skill version:** 1.2.5  
**Core Specs baseline:** 2.5  
**AI Index baseline:** 7.4  
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

The package boundary remains explicit: the Open Edition is fully usable on its own, while selected Stephan A. Davis model and framework pages may be used only as optional external semantic context.

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

## Core v2.5 alignment and version cue

Skill **1.2.5** embeds the complete approved **Stable Core Specs 2.5**, its YAML-TXT mirror, Logic, source README and Guidance without content changes. The `2.5` suffix is a deliberate maintainer-requested version cue. Skill and Core remain independently versioned: the metadata explicitly records the actual baseline, and no intermediate Skill releases or automatic future compatibility are implied.

The runtime adapter implements contextual evidence classes, scoped/revocable process consent, requested pattern reflection, question budgets, clear reasoned recommendations, proportionate stabilization, mixed-request safety routing and calibrated referral. The optional Resonanzkreis adds external context without introducing a mandatory workflow, replacing ACR or changing consent/safety authority.

Embedded upstream documents retain their original freeze-time statuses and relative paths. `references/README_v2.5.md` is the unchanged upstream `README.md`, not this Skill's installation guide; paths inside it refer to the original Public Bundle. `SOURCE-MATERIAL-NOTICES.md` describes the local mapping and the exact subset bundled here.

## Evaluation and release evidence

Use `evals/release-evidence-v1.2.5.json` for checks actually executed for this Skill. The previous private-integration evidence in `evals/core-specs-v2.5/` remains historical and is not credited as execution on this Skill or a new host.

- `evals/evals.json`: bilingual Skill regression inventory.
- `evals/description-trigger-evals.json`: activation and mode-routing inventory.
- `evals/core-specs-v2.5/scenarios_v2.5.yaml` and `.md`: all 45 authored upstream cases, byte-identical.
- `evals/behavioral-probes-v1.2.5.json`: bounded synthetic output probes, if executed and recorded.
- `scripts/validate_release_evidence.py`: full JSON Schema validation.
- `scripts/validate_evals.py`: inventory and semantic evidence consistency.
- `scripts/validate_package.py`: source/version/rights/security and checksum validation.

Keep evaluation prompts, expected criteria, gold principles and audit evidence out of the target runtime context. Inventory validation is not behavioral execution. Small synthetic probes are not a complete multilingual or multi-host deployment validation. Refer to the actual release evidence for status and limitations.

## Source hierarchy

1. `references/auren-core-specs_v2.5.yaml`
2. `references/auren-core-logic_v2.5.md`
3. `references/README_v2.5.md`
4. `references/Guidance4AIsystems_v2.5.txt`
5. external AI Index as supplementary semantic context only
6. optional semantic references from `OPTIONAL-SEMANTIC-REFERENCES.json` as non-operational external context only

The embedded YAML remains the operational source of truth.

## Remote currentness

The update checker retains its fixed `stephanadavis.de` HTTPS/443 allowlist, GET-only/no-user-content policy, full redirect validation and detect/report-only behavior. It checks the AI Index v7.4 baseline, versioned website README and Guidance, and the pinned v2.5 YAML-TXT together with the moving website mirror.

The supplied canonical Core Logic v2.5 link is pinned on `raw.githubusercontent.com`, outside that fixed checker allowlist. It is recorded as `manual_host_review_only`: the checker makes no request to it and reports unavailable currentness. An appropriately authorized host may review the published pinned link separately. This does not broaden the automatic checker or authorize runtime fetching. Network failures leave the local approved sources active without a fresh-currentness claim.

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
│   ├── release-evidence-v1.2.5.json
│   └── RELEASE-EVIDENCE.md
├── examples/
└── scripts/
```
