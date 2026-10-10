# AUREN Core Skill Rights, License, and Edition Matrix

**Version:** 1.4  
**Date:** 2026-10-10  
**Owner:** Stephan A. Davis  
**Status:** binding build basis for AUREN Core Skill 1.2.5 — Open Edition

## Architecture decision

The public release is the AUREN Core Skill **Open Edition** with Runtime, Integration, and Audit modes. It embeds only explicitly open Core material and newly created open package files. It does not embed proprietary methodologies, internal resources, or the public AUREN CustomGPT knowledge base.

Package licensing is file-type specific:

- content, documentation, specifications, examples, and content evals: CC BY-SA 4.0;
- validators, checker code, and tests: MIT;
- names, official edition identity, trademarks, optional linked proprietary models, and external resources: separate rights or external terms.

## Source hierarchy

1. AUREN Core Specs v2.5 YAML.
2. AUREN Core Logic v2.5.
3. AUREN Core README v2.5.
4. Guidance for AI Systems v2.5.
5. AI Index v7.4 as external semantic context.
6. Optional semantic references from `OPTIONAL-SEMANTIC-REFERENCES.json` as non-operational external context.
7. Historical analysis and prior functional-handoff material as provenance only, not packaged; the public Core v2.5 integration handoff is included separately.

## Resource matrix

| ID | Resource | Role | Rights | Open Edition decision |
|---|---|---|---|---|
| AUR-001 | AUREN Core Specs v2.5 | operational source of truth | CC BY-SA 4.0 | embedded, pinned |
| AUR-002 | AUREN Core Logic v2.5 | operational narrative | CC BY-SA 4.0 | embedded; YAML wins on conflict |
| AUR-003 | AUREN Core README v2.5 | semantics and source documentation | CC BY-SA 4.0 | embedded |
| AUR-004 | Guidance for AI Systems v2.5 | supplementary policy | CC BY-SA 4.0 | embedded |
| AUR-005 | AI Index v7.4 | external semantic context | resource-specific; no package-wide license inferred | linked, not embedded |
| AUR-006 | unversioned Core Specs alias | update detection | external CC source | linked only |
| AUR-007 | three additional prompt-reflection questions | possible later extension | public license not explicitly confirmed | excluded from the Open Edition until an explicit public license decision exists |
| AUR-008 | AUREN name and official identity | brand/name layer | separately reserved | use subject to notice |
| AUR-009 | Triarchy of Systemic Leadership | proprietary methodology | proprietary | optional canonical reference; not embedded; no reconstruction |
| AUR-010 | WORT-Prinzip | proprietary methodology | proprietary | optional canonical reference; not embedded; no reconstruction |
| AUR-011 | Konsequenzen-Kompass | proprietary methodology | proprietary | optional canonical reference; not embedded; no reconstruction |
| AUR-012 | Einfluss-Formel | proprietary methodology | proprietary | optional canonical reference; not embedded; no reconstruction |
| AUR-013 | ACR cycle as expressly published in Core v2.5 | runtime component | CC BY-SA 4.0 within Core sources | embedded only in published Core form |
| AUR-014 | complete ACR Attendancy methodology | proprietary methodology | proprietary | excluded; no derivation claim |
| AUR-015 | public framework pages | semantic context | external terms | links and attribution only |
| AUR-016 | mentoring, practitioner, training, workbook, scoring, facilitation, and certification material | proprietary resources | proprietary | excluded |
| AUR-017 | public AUREN CustomGPT configuration and knowledge base | separate product/runtime | separate platform and owner terms | external only; no equality claim |
| AUR-018 | historical analysis | provenance | source material only | not embedded |
| AUR-019 | functional handoff | provenance | source material only | not embedded |
| AUR-020 | internal governance policy | internal policy | no public license | not embedded; public governance newly written |
| AUR-021 | public package documentation, examples, and content evals | package content | CC BY-SA 4.0 | embedded |
| AUR-022 | validators, build/check scripts, and test code | tooling | MIT | embedded |
| AUR-023 | synthetic gold evals | quality assurance | CC BY-SA 4.0 for content; MIT for code | embedded and marked synthetic |
| AUR-024 | real or anonymized dialogue examples | optional evidence | separate permission required | excluded until approved |
| AUR-025 | Resonanzkreis | optional reflection/action/feedback context | external terms | canonical link only; no bundled methodology or mandatory workflow |

## Edition distinction

| Feature | Open Edition Skill | Public AUREN CustomGPT | Internal Edition | Mentee Companion |
|---|---|---|---|---|
| Distribution line | public Open Edition | separate existing product | private/owner line | separate private product line |
| Purpose | portable Runtime, Integration, and Audit core | canonical public chat experience | owner working environment | bounded between-session reflection |
| Proprietary models | not embedded | according to its own configuration | may be included | only expressly approved subsets |
| CustomGPT knowledge base | not included | present | optional, separate | not automatically included |
| Final judgement/accountability takeover | prohibited | prohibited | prohibited | prohibited |
| Diagnosis or therapy | prohibited | prohibited | prohibited | prohibited |

## Derivative rule

Modified versions must identify changes, preserve CC attribution and ShareAlike obligations for covered content, and avoid implying official status or endorsement. Creative Commons licensing does not grant trademark or official-edition rights.

## Build consequences

- Pin the v2.5 YAML as operational source of truth.
- Embed Logic, source README, and Guidance under CC BY-SA 4.0.
- Register AI Index v7.4 externally without a bundled snapshot.
- Compare the pinned YAML-TXT with the moving website mirror during currentness checks and require equivalence.
- Keep proprietary methodologies and the CustomGPT knowledge base out of the package.
- Catalog selected public model/framework pages as optional semantic references without bundling or relicensing them.
- Keep the Open Edition fully functional when every optional reference is unavailable.
- Apply MIT only to scripts and test code.
- Record an omission rationale for each known excluded source.
- Keep the three additional reflection questions out of the Open Edition until their license decision is explicit.


## Open Edition semantic-extension rule

The Open Edition may point to selected owner-maintained external framework pages through `OPTIONAL-SEMANTIC-REFERENCES.json`. The catalog is metadata only. It does not reproduce the referenced methodologies, make them required dependencies, or apply the package CC BY-SA license to them. External references may enrich context but may never override the embedded Core Specs, safety, privacy, or human-responsibility rules.
