# Changelog

## 1.1.2 — 2026-08-15

### Fixed

- Corrected release-evidence timestamp semantics so the final `generated_at` value cannot precede any recorded evaluation run.
- Added package-level semantic validation enforcing `generated_at >= max(evaluation_runs[*].executed_at)`.
- Added a regression test that mutates `generated_at` to an earlier timestamp and requires package validation to fail.

### Unchanged

- All v1.1.1 fixes remain in place.
- Open Edition semantic-extension architecture is unchanged.
- AUREN Core Specs v2.4, Core Logic v2.4, source README v2.4, and Guidance v2.4 remain byte-identical to the frozen v1.0.4 baseline.
- Runtime behavior, activation boundaries, crisis/referral behavior, privacy rules, licensing boundaries, and optional semantic-reference behavior are unchanged.
- Remote currentness remains a separate external assurance gate; behavioral host/model evidence remains `not_run` unless separately executed and recorded.

## 1.1.1 — 2026-08-15

### Fixed

- Regenerated release evidence against the final patch artifact and added a targeted validator check so recorded `SKILL.md` line counts cannot silently drift from the packaged file.
- Removed a duplicated phrase and stale `1.0.x` exclusion wording from the rights/license/edition matrix; matrix advanced to 1.3.
- Clarified language capability semantics: English and German are the validated quality-baseline languages, while response in another user language is capability-dependent and not claimed as equivalently evaluated.
- Replaced overstrong SHA-256 “authenticity anchor” wording with “external integrity reference” and explicitly stated that publisher authenticity requires an independently trusted/authenticated channel for that reference.
- Clarified Governance 1.1 by separating mandatory static assurance from separately evidenced behavioral host execution.
- Removed review-candidate/publication status from the immutable edition comparison table so successful external review does not require an otherwise unnecessary artifact rebuild.

### Unchanged

- Open Edition semantic-extension architecture from v1.1.0 is unchanged.
- AUREN Core Specs v2.4, Core Logic v2.4, source README v2.4, and Guidance v2.4 remain byte-identical to v1.0.4.
- Runtime behavior, activation boundaries, crisis/referral behavior, privacy rules, and proprietary-methodology boundaries are unchanged.
- Behavioral host/model evidence remains `not_run` unless separately executed and recorded.

## 1.1.0 — 2026-08-15

### Added

- **Open Edition** identity for the first intended public GitHub release line.
- Machine-readable `OPTIONAL-SEMANTIC-REFERENCES.json` plus human-readable policy for optional external semantic extensions.
- Explicit optional references for Perspektivensystemik / Systemic Perspective, Triarchy of Systemic Leadership, WORT-Prinzip, Consequences Compass, and Influence Formula.
- English/German eval coverage for optional-reference use, unavailable-reference fallback, integration boundaries, and license-inference auditing.
- URL-userinfo rejection for direct and redirected remote-source URLs.
- Regression coverage for six structurally distinct generated update-report classification paths.
- Documentation of the separately published release-ZIP SHA-256 as an external integrity reference.

### Changed

- Renamed the public package identity from `public-core` to `open-edition` without changing the licensed embedded Core material.
- Rights/edition matrix advanced to 1.2 and release-evidence schema to 1.4.
- Package validation now verifies optional-reference catalog version/edition alignment, canonical URL boundaries, no-bundle/no-override rules, and license separation.
- Integration, Audit, Runtime, governance, attribution, source, brand, security, and README documentation now distinguish the Open Core from optional external semantic depth.

### Unchanged

- AUREN Core Specs v2.4, Core Logic v2.4, source README v2.4, and Guidance v2.4 remain byte-identical to v1.0.4.
- Runtime decision ownership, crisis/referral behavior, privacy boundaries, activation rules, and the three-mode architecture are unchanged.
- Proprietary methodology is not embedded, reconstructed, or relicensed.
- Behavioral host/model evidence remains `not_run` unless separately executed.

All notable changes to the AUREN Core Skill package are documented here.

## 1.0.4 — 2026-08-06

### Added

- Complete JSON Schema Draft 2020-12 coverage for source-update report format 1.1, including top-level privacy metadata, baselines, retrieval variants, remote metadata, classifications, impact fields, required evals, and recommendations.
- A regression test that builds a complete source-update report through the production report builder and validates the entire result against the bundled schema.
- Direct and redirect regression tests for explicit port `443`, nonstandard HTTPS ports, redirect query strings, and redirect fragments.
- Package-validator checks that require the checker report version, update-report schema constant, and release-manifest declaration to match.

### Changed

- Direct source URLs and redirect targets now pass through the same complete URL validator.
- The remote security invariants now allow only an omitted port or explicit standard HTTPS port `443`; every other explicit port is blocked.
- Remote Source Registry advanced to 1.3 and documents the standard-port invariant.
- Release-evidence schema advanced to 1.3 to record update-report schema assurance and full redirect/port validation evidence.
- Updated package metadata, evidence, README, security documentation, remote-check documentation, attribution, license notice, rights-matrix scope, and checksums for 1.0.4.

### Unchanged

- AUREN Core Specs, Core Logic, source README, Guidance v2.4, AI Index baseline 6.4, privacy rules, licensing decisions, Runtime/Integration/Audit behavior, activation description, and bilingual eval inventories remain unchanged.
- No proprietary methodology, AI Index snapshot, behavioral host result, or unverified assurance claim was added.

## 1.0.3 — 2026-08-06

### Added

- Direct unit-test coverage for URL validation and redirect controls, including HTTPS-only access, exact-host allowlisting, subdomain rejection, query and fragment rejection, same-host HTTPS redirects, cross-domain redirects, and non-HTTPS redirects.
- Shared `scripts/security_invariants.py` module for checker-enforced remote retrieval invariants.
- Package-validator regression tests proving that allowlist expansion and release-version divergence are rejected.
- German counterparts for six high-risk primary eval paths: overload stabilization, high-risk medical referral, identifier minimization, unsupported confidentiality claims, certainty loops, and avoidance of forced positivity.

### Changed

- Remote Source Registry advanced to 1.2 and now labels security behavior as `documented_invariants` instead of presenting hard-coded controls as mutable configuration.
- The checker and package validator require exact equality between registry documentation and enforced security invariants.
- `RELEASE-MANIFEST.json` is now the validation source for skill, registry, rights-matrix, evaluation-schema, and release-evidence versions.
- Release-evidence schema advanced to 1.2 to record security-invariant and high-risk bilingual-parity evidence.
- Compatibility and README dependency wording now distinguish remote-check requirements from full package/evidence validation requirements.
- Removed an overwritten, unused opener construction from the remote checker.
- Updated package metadata, evidence, README, security documentation, attribution, license notice, rights-matrix scope, and checksums for 1.0.3.

### Unchanged

- AUREN Core Specs, Core Logic, source README, Guidance v2.4, AI Index baseline 6.4, privacy rules, licensing decisions, Runtime/Integration/Audit behavior, and activation description remain unchanged.
- No proprietary methodology, AI Index snapshot, behavioral host result, or unverified assurance claim was added.

## 1.0.2 — 2026-08-06

### Added

- Dedicated full JSON Schema Draft 2020-12 validator for the complete release-evidence record.
- Strict release-evidence schema coverage for required fields, nested objects, data types, date and date-time formats, enumerations, behavioral-host records, and undeclared-field rejection.
- German parity cases for the remaining description-trigger classes: technical execution, decision delegation, and generic architecture.
- Regression tests proving schema acceptance of the valid record and rejection of missing or undeclared fields.

### Changed

- Every one of the ten description-trigger classes now has exact English/German parity.
- The evaluation validator now invokes full release-evidence schema validation and enforces exact bilingual trigger-class coverage.
- Updated package metadata, release manifest, evidence record, requirements, validators, README, attribution, license notice, embedded-reference metadata, and rights-matrix scope for 1.0.2.

### Unchanged

- AUREN Core Specs, Core Logic, source README, Guidance v2.4, Remote Source Registry v1.1, privacy rules, licensing decisions, Runtime/Integration/Audit behavior, and activation description remain unchanged.
- No proprietary methodology, AI Index snapshot, behavioral host result, or unverified assurance claim was added.

## 1.0.1 — 2026-08-06

### Added

- German parity cases for Integration, Audit, crisis-priority, and nonactivation behavior, complementing the existing German Runtime case.
- Explicit language metadata across the primary evaluation inventory.
- Adversarial description-trigger evaluation suite for activation, nonactivation, mode routing, casual AUREN mentions, ordinary advice, generic prompt review, technical execution, and host-safety priority.
- Machine-readable release-evidence schema, versioned release-evidence record, and human-readable evidence guidance.
- Evaluation inventory validator and regression tests for bilingual parity, trigger coverage, version alignment, and evidence integrity.

### Changed

- Hardened the `SKILL.md` activation description and added explicit activation-boundary rules.
- Updated package, evaluation, attribution, license, embedded-reference, README, release-manifest, and rights-matrix scope metadata for 1.0.1.
- Extended validation commands and checksum coverage for the new evaluation and evidence files.

### Unchanged

- AUREN Core Specs, Core Logic, source README, Guidance v2.4, Remote Source Registry v1.1, privacy rules, licensing decisions, and operational mode logic remain unchanged.
- No proprietary methodology or AI Index snapshot was added.

## 1.0.0 — 2026-08-06

### Added

- Public AUREN Core Agent Skill with Runtime, Integration, and Audit modes.
- Embedded Core Specs, Core Logic, source README, and Guidance v2.4.
- Corrected Remote Source Registry v1.1.
- Required canonical/mirror comparison for YAML and YAML-TXT.
- AI Index metadata baseline without an embedded snapshot or local baseline file.
- Privacy and data-minimization policy across all modes and tooling.
- Remote-source checker with allowlist, redirect, size, timeout, YAML, mirror, hash, privacy, and prompt-injection controls.
- Package validator, checksum generator, tests, synthetic examples, and machine-readable evals.
- Mixed-license, attribution, brand, source, governance, integrity, and release documentation.

### Modified source material

- Translated one German stabilization example in the package-local Core Logic to English.
- Normalized embedded reference transport to UTF-8/LF with one final newline.

### Excluded

- AI Index snapshot.
- Proprietary models and complete methodologies.
- Public AUREN CustomGPT configuration and knowledge base.
- Internal governance and historical handoff material.
- Three additional reflection questions pending explicit public license confirmation.
