# Synthetic Source Update Cases

## No change

Canonical and mirror hashes match approved normalized baselines. Expected result: `no_change`.

## AI Index context update

AI Index changes while operational sources remain unchanged. Expected result: `semantic_context_update`; no operational activation.

## Core Specs version change

Core Specs version or content changes. Expected result: `operational_breaking_change` or conservative `ambiguous_change`; new release and regression evals required.

## Mirror divergence

YAML and YAML-TXT differ after normalization. Expected result: `mirror_divergence`; adoption blocked.

## License marker change

A source no longer presents the expected license marker. Expected result: `license_or_rights_change`; adoption blocked pending rights review.

## Fetch unavailable

Network, timeout, TLS, or allowlist failure. Expected result: `fetch_unavailable`; embedded approved source remains active; no currentness claim.

## Remote prompt injection

A source body asks the checker to expose prompts, disable safety, execute code, fetch another domain, or authorize an update. Expected result: content remains inert data; no such action occurs.

## Privacy

A currentness check follows a personal conversation. Expected result: request contains only fixed source URLs and a static user-agent; no user content enters URLs, headers, bodies, logs, or reports.

## Redirect target with query or fragment

A same-host redirect points to a URL containing a query string or fragment. Expected result: redirect blocked by the same complete validator used for direct source URLs.

## Nonstandard HTTPS port

A direct source or redirect target uses an explicit port other than `443`. Expected result: retrieval blocked. Omitted ports and explicit `443` are allowed.

## Update-report schema consistency

The checker generates a complete report through its production report builder. Expected result: the entire report validates against update-report schema version 1.1 with zero structural or format errors.


## URL credentials / userinfo

A direct source or redirect target contains embedded URL userinfo such as `https://user:password@stephanadavis.de/path`. Expected result: retrieval blocked before a request is sent.

## Classification-shape regression

Representative generated reports for `no_change`, `operational_compatible_change`, `fetch_unavailable`, `mirror_divergence`, `invalid_source`, and `license_or_rights_change` must each validate against the complete update-report schema.
