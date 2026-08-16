# Release Evidence

Release evidence records what was actually validated for a specific AUREN Core Skill release. It must not imply that a model, host, or deployment was tested when no such run occurred.

## Evidence layers

1. **Structural schema validation** checks the complete evidence document against `release-evidence.schema.json` using JSON Schema Draft 2020-12 and format checking.
2. **Semantic inventory validation** checks manifest-derived version alignment, unique IDs, bilingual coverage, high-risk path parity, trigger-class parity, and consistency rules that are not fully expressible in JSON Schema.
3. **Static package validation** checks required files, source integrity, exact security invariants, privacy boundaries, licensing metadata, release metadata, and checksums.
4. **Unit tests** exercise validators, URL validation, redirect behavior, registry-mutation rejection, and update-check behavior.
5. **Behavioral host evidence** may be added only after the eval cases have actually been executed on named hosts and models.
6. **Manual review** records qualitative review scope without representing it as model execution.

## Version 1.1.2

`release-evidence-v1.1.2.json` records the build-time evidence for this patch-level Open Edition release. The complete record is structurally validated against release-evidence schema version 1.4. Package validation additionally enforces temporal evidence consistency: the final `generated_at` timestamp must be greater than or equal to every recorded `evaluation_runs[*].executed_at` timestamp. A complete checker-generated source-update report is separately validated against update-report schema version 1.1. Direct requests and redirect targets share one full URL-validation path, including query, fragment, hostname, scheme, and standard-port enforcement. Behavioral model and host evidence remains explicitly marked `not_run`.

## Future host evidence

For each actual host or model run, record the host and model identifiers, versions, execution time, number of cases, pass/fail/manual-review outcomes, and an evidence reference. Do not replace failed or partial outcomes with a narrative success claim.

Version 1.1.2 preserves the v1.1.0 optional semantic-reference and URL/security assurance, carries forward the v1.1.1 evidence/artifact alignment guards, and adds a temporal guard so a final evidence record cannot claim to have been generated before the runs it records.
