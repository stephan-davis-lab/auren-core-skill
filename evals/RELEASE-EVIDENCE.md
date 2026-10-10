# Release Evidence

Release evidence records what was actually validated for a specific AUREN Core Skill release. It must not imply that a model, host, or deployment was tested when no such run occurred.

## Evidence layers

1. **Structural schema validation** checks the complete evidence document against `release-evidence.schema.json` using JSON Schema Draft 2020-12 and format checking.
2. **Semantic inventory validation** checks manifest-derived version alignment, unique IDs, bilingual coverage, high-risk path parity, trigger-class parity, and consistency rules that are not fully expressible in JSON Schema.
3. **Static package validation** checks required files, source integrity, exact security invariants, privacy boundaries, licensing metadata, release metadata, and checksums.
4. **Unit tests** exercise validators, URL validation, redirect behavior, registry-mutation rejection, and update-check behavior.
5. **Behavioral host evidence** may be added only after the eval cases have actually been executed on named hosts and models.
6. **Manual review** records qualitative review scope without representing it as model execution.

## Version 1.2.5

`release-evidence-v1.2.5.json` records the checks performed for this Core 2.5 Skill integration. Read its per-run status and evidence references. The unchanged upstream private-integration summary is separate historical evidence; none of its model runs counts as execution of this Skill revision.

Bounded fresh-context synthetic probes, when recorded, constitute partial behavioral evidence with original prompts and outputs. Their exact internal model and host versions may be unavailable and must be marked unknown. They do not replace execution of the full bilingual Skill inventories or all 45 canonical Core cases on target hosts.

Evidence timestamps, current SKILL.md line count, source identity, catalog count and inventory versions must match the final artifact. Keep evaluation material outside operational runtime loading.
