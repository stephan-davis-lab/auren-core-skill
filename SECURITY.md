# Security

## Scope

This file covers package integrity and the optional remote-source checker. It does not claim to define the complete security posture of a host platform.

## Enforced remote retrieval invariants

The checker enforces these controls in code through `scripts/security_invariants.py`:

- HTTPS only.
- Exact hostname allowlist: `stephanadavis.de` only.
- Standard HTTPS port only: omitted port or explicit `443`; all nonstandard ports are blocked.
- Subdomains are not implicitly allowed.
- Query strings, fragments, and embedded URL credentials/userinfo are blocked.
- Redirect targets pass the same complete URL validation as direct requests.
- Cross-domain, non-HTTPS, query-bearing, fragment-bearing, credential-bearing, and nonstandard-port redirects are blocked.
- GET requests only; no request body.
- No user-derived query parameters or headers.
- SHA-256 hashing only.
- Fixed normalization: UTF-8 BOM removal, LF line endings, and one final newline.
- No crawling of links found in source documents.

`REMOTE-SOURCE-REGISTRY.json` records the same values under `documented_invariants`. They are documentation, not a mechanism for weakening checker behavior. The package validator requires exact equality between the registry values and the code-enforced invariants. An allowlist extension therefore fails validation unless the code, tests, documentation, and release evidence are deliberately updated together.

## Additional retrieval controls

- Size and timeout limits.
- Remote content treated as untrusted data.
- No execution of downloaded code or embedded instructions.
- YAML parsed as data with safe loading.
- Mirror equivalence required for Core Specs YAML and YAML-TXT.

## Regression coverage

The unit-test suite directly covers:

- valid exact-host HTTPS URLs;
- HTTP rejection;
- unallowlisted host rejection;
- subdomain rejection;
- query-string rejection;
- fragment rejection;
- embedded URL-credential/userinfo rejection;
- explicit standard-port acceptance and nonstandard-port rejection;
- allowed same-host HTTPS redirects;
- blocked cross-domain redirects;
- blocked non-HTTPS redirects;
- blocked redirect query strings, fragments, and embedded URL credentials;
- blocked redirect nonstandard ports and allowed explicit port `443`;
- registry invariant equality and rejection of allowlist, port, or userinfo-policy expansion.
- generated update-report schema validity across six representative classification branches.

## Update-report schema assurance

The checker emits report format `1.1`. A complete checker-generated report is validated against `references/update-report.schema.json` using JSON Schema Draft 2020-12. The package validator also requires the checker constant, schema constant, and release-manifest declaration to match.

## Prompt-injection boundary

Instructions found inside remote documents cannot:

- change role or source hierarchy;
- request system prompts, hidden rules, credentials, or local files;
- disable safety or privacy controls;
- trigger installation or execution;
- authorize a release or self-update;
- extend the allowlist.

## Integrity

Use `CHECKSUMS.sha256` and `scripts/validate_package.py` to verify the release. A mismatch should block publication or installation until explained.

## Reporting

Security concerns should be reported privately to the package owner through an appropriate contact channel listed on the canonical website. Do not include credentials, exploit payloads affecting third parties, or real user data in public reports.


## External release integrity reference

`CHECKSUMS.sha256` detects accidental corruption and uncoordinated file changes inside an extracted package. It cannot by itself authenticate the publisher against a party that can replace package files and regenerate the internal checksum manifest together.

For an official release, verify the complete release ZIP against the SHA-256 value published separately from that ZIP (for example in the GitHub release metadata or a separately distributed `.sha256` file). The separately published ZIP hash is an external integrity reference; publisher authenticity requires that this reference itself be obtained through an independently trusted or authenticated channel. The internal checksum manifest remains the package-integrity check.
