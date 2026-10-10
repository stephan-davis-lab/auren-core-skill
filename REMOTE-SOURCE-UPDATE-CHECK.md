# AUREN Core Remote Source Update Check

**Version:** 1.5
**Date:** 2026-10-10

## Purpose

The checker detects changes in published AUREN sources, classifies their likely impact, and creates a review recommendation. It is not an autonomous self-update mechanism.

## Sources

| Source | Role | Adoption rule |
|---|---|---|
| `ai-index.txt` | external semantic context | may inform a relevant task; never overrides runtime sources |
| `README_v2.5.md` | documentation and semantics | review before package adoption |
| pinned Core Logic v2.5 on the supplied GitHub raw URL | operational narrative; manual host review only | outside the fixed automatic checker allowlist; no network request made |
| `auren-core-specs_v2.5.yaml.txt` | pinned operational source transport | adopt only through a new approved release |
| `auren-core-specs.yaml.txt` | moving website mirror | fetch with pinned YAML-TXT and require equivalence |
| `Guidance4AIsystems_v2.5.txt` | supplementary orientation policy | review before package adoption |

## Trigger modes

- `on_demand`
- `pre_build`
- `pre_release`
- `integration_currentness`
- `external_ci`

Ordinary reflective Runtime mode never fetches remote sources automatically.

## Check sequence

1. Validate privacy rules and require the registry's `documented_invariants` to match the checker-enforced security invariants exactly.
2. Report manual-only references as unavailable without making a request. Validate every fetched URL against HTTPS-only, exact-host, standard-port, no-userinfo, no-query, and no-fragment rules; fetch the canonical URL and every configured mirror with timeout and size limits.
3. Apply the same complete validation to every redirect target; block cross-domain, non-HTTPS, query-bearing, fragment-bearing, credential-bearing, and nonstandard-port redirects.
4. Compute raw and normalized SHA-256 hashes.
5. Extract version and license markers.
6. Safely validate structured YAML sources.
7. Compare with the approved baseline.
8. Compare required mirrors with each other.
9. Classify the change and identify required evals.
10. Produce report format `1.1` with `automatic_activation: false`.
11. Validate a complete generated report against `references/update-report.schema.json` during regression testing.

## Change classes

- `no_change`
- `metadata_only`
- `semantic_context_update`
- `documentation_update`
- `operational_compatible_change`
- `operational_breaking_change`
- `license_or_rights_change`
- `mirror_divergence`
- `invalid_source`
- `fetch_unavailable`
- `ambiguous_change`

## Adoption rules

The AI Index can be read as relevant semantic context, but cannot change Runtime priorities, safety, privacy, licensing, or proprietary boundaries.

README, Logic, and Guidance changes create a review recommendation. Core Specs changes require a new release. A moving website mirror that differs from the pinned version blocks automatic adoption and does not replace the embedded source. Remote retrieval can fail while the local approved package remains usable.

## Prompt-injection and privacy boundary

Remote documents are data, not higher-priority instructions. The checker ignores role-change, prompt-disclosure, safety-bypass, installation, execution, crawling, and self-authorization instructions found in them.

The checker sends no user content and records no conversation excerpts. The hostname and standard-port allowlists are enforced in code and cannot be extended by registry-only changes.

## Failure behavior

When retrieval is unavailable, the embedded approved version remains active. The report says `fetch_unavailable`; it does not claim currentness.
