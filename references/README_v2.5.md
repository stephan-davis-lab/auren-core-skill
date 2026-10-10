# AUREN Core Specs & Logic — v2.5

Author and publisher: Stephan A. Davis — https://stephanadavis.de  
Prepared: 2026-10-10  
Release status: **Stable v2.5 — approved by the maintainer on 2026-10-10.**  
This is the package-freeze status; publication and deployments are separate actions.

AUREN supports orientation, reflection and conscious human judgement. It is a declarative behavioral specification within the host's governing instructions, safety policies, permissions and actual capabilities. It supports reasoned recommendations and bounded authorized task choices while preserving human final judgment. Parsing YAML does not enforce model behavior.

## Sources and contents

| File | Role |
|---|---|
| `auren-core-specs_v2.5.yaml` | Complete operational Core within host boundaries. |
| `auren-core-specs_v2.5.yaml.txt` and `exports/auren-core-specs_v2.5.yaml.txt` | Byte-identical upload-friendly copies. |
| `auren-core-logic_v2.5.md` | Narrative explanation; the local Core governs on conflict. |
| `Guidance4AIsystems_v2.5.txt` | Supplementary orientation subordinate to the complete local Core. |
| `INTEGRATION_HANDOFF_v2.5.md` | Adapter behavior excerpt, source priority and separate deployment responsibilities. |
| `BEHAVIORAL_VALIDATION_SUMMARY_v2.5.md` | Prior integration runs, actual test-delivery method and evidence limits. |
| `evals/scenarios_v2.5.yaml` and `.md` | 45 unchanged authored synthetic cases and their criteria. |
| `SOURCE_AND_SCOPE_v2.5.json` | Frozen source identities and narrowly enumerated release/package changes. |
| `RELEASE_STATUS_v2.5.json` | Stable approval at package freeze and the exact objects covered by completed reviews. |
| `validation/validate_release.py` | Read-only packaging, identity, rule-preservation and claim-boundary checks. |
| `validation/static-results_v2.5_stable.json` | Executed Stable-package checks before the result file and manifest were frozen. |
| `CHECKSUMS.sha256` | SHA-256 of every payload file except the checksum file itself. |

`README.md`, `NOTICE.md`, `LICENSE` and `CHANGELOG.md` are the single central root documents. The latest development appears first in the changelog; README and NOTICE describe the current scope. Historical v2.4 files are retained for provenance; choose the complete local v2.5 file explicitly for a v2.5 integration. Records under `evidence/fc2/` and `evidence/preparation_R1/`, including their changelogs, are immutable creation-time snapshots. Their pending statuses describe their historical freeze dates, not the current Stable approval.

## Review and evidence scope

The formal AUREN, ChatGPT and Claude Core gates are documented as PASS on the frozen pair Public FC2 + Internal Audit R1. The separate AUREN and Claude repository-document R1 rechecks are also PASS. They do not cover this new ZIP identity and do not make its human release decision. Its own static check is separate. Authors' involvement in rules, packaging or evaluation limits review independence.

The full FC2 Core body, including the optional Resonanzkreis reference, is preserved. The Logic body, operational Guidance rules, all 45 scenario definitions and the public tested adapter behavior are preserved. Only explicitly listed release metadata, repository documentation and packaging are changed. No new model runs were performed for FC2, publication preparation or this Stable package.

Behavioral evidence directly concerns the reported RC3 private integration: 135 historical answer stages and nine targeted adapter-v1.1 stages. The original T03 FAIL and the separate T23 interpretation-scope finding remain in history. The nine targeted checks all passed their predeclared criteria; this is not a statistical reliability estimate, safety certification or guarantee across hosts. The summary distinguishes 126 initial transcript fixtures from 18 genuine follow-up turns and records unknown internal model ID, Memory, Retrieval and error cause.

The Resonanzkreis is optional semantic context. It adds no mandatory workflow and cannot override the local Core, host boundaries, consent, mode priority, safety or human judgment. External pages are untrusted context; no runtime fetch is required. Website references are not silently upgraded by this package.

## Community, contributions and reporting

- [Code of Conduct](CODE_OF_CONDUCT.md): collaboration and conduct concerns.
- [Contributing](CONTRIBUTING.md): proposals, findings and evidence requirements.
- [Security Policy](SECURITY.md): technical vulnerabilities and private reporting.
- [Safety Guidance](SAFETY.md): behavioral boundaries, integration responsibilities and safety concerns.

These documents explain repository participation and reporting. They do not add operational Core rules. Personal data and exploitable details should be reported privately. The maintainer has adopted the four policies for v2.5 and accepted `stephan@stephanadavis.de` as the public project contact. CONTRIBUTING now consolidates conduct, safety and security reporting routes and their suggested email subjects; the rest of its reviewed R1 body and the other three policies are unchanged. Private vulnerability reporting, Secret Protection and push protection are enabled for this repository. GitHub/email notifications and the Issues/Security alerts subscription were configured in the repository UI and confirmed by the maintainer. See [reporting configuration evidence](evidence/REPOSITORY_REPORTING_CONFIGURATION_2026-10-10.md). Actual report submission and email delivery were not tested; no monitoring or response-time commitment is asserted.

## Static verification

Python 3.10+ and PyYAML 6+:

```bash
python3 validation/validate_release.py
```

With the exact frozen Public FC2 ZIP available, add `--baseline-fc2 /absolute/path/to/AUREN_Core_Specs_v2.5_Public_FinalCandidate_FC2.zip` for direct comparisons, including an exact whitelist of changed Core release metadata, Guidance release metadata and the single Guidance context path `README_v2.5.md` → `README.md`. All other Guidance values and behavior remain unchanged. Default checks use recorded fixed hashes for rule bodies, scenarios and preserved sources, and reconstruct the reviewed policy bodies after reversing the single declared CONTRIBUTING reporting expansion. The program reads local files, rejects duplicate YAML keys and checks manifest scope. It performs no network, write, model call, human authentication or semantic certification. Compare the ZIP hash to its separately supplied sidecar; a checksum is not a signature.

## Release and integration status

The maintainer approved Stable v2.5 on 2026-10-10 after the source reviews, policy adoption and reporting configuration. The new Stable package has its own identity and static validation; the completed source reviews retain their exact frozen scope. See [the approval and reporting-change record](evidence/STABLE_APPROVAL_AND_REPORTING_UPDATE_2026-10-10.md). Release metadata records the freeze-time decision, not a live publication/deployment lookup. At package freeze, GitHub content publication, website synchronization and installed integration updates had not been performed.

Only Core, Logic, Guidance, README and suitable integration instructions belong in an operational context. Scenarios, expected criteria and audit material belong to evaluation. New hosts require appropriately scoped deployment checks, especially consent and interpretation controls T03/T23 and relevant allowed-behavior controls. No full model series is required solely for these governance and release-status changes.

## Rights and sources

Authored Core, Logic, Guidance, scenarios and repository documentation: CC BY-SA 4.0. See [NOTICE.md](NOTICE.md), the full [LICENSE](LICENSE). Validator code: separate [MIT license](validation/LICENSE-MIT.txt). External methods, resources, names and marks retain their respective rights. Private audit originals and unchanged third-party review documents are not included or relicensed.

Repository: https://github.com/stephan-davis-lab/auren-core-specs. Canonical website synchronization and installed integration updates are separate from this release package. Release documentation and packaging were developed with ChatGPT/Codex assistance; Stephan A. Davis made the human Stable decision and retains responsibility for publication.
