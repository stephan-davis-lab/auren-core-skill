# Privacy and Data Minimization

**Version:** 1.0  
**Applies to:** all AUREN Core Skill modes and tooling

## Purpose

AUREN Core supports reflection without creating unnecessary data exposure. The skill minimizes requested, repeated, transmitted, logged, and retained personal information.

## Runtime rules

1. Ask only for information needed to understand the current task.
2. Prefer roles, placeholders, ranges, and paraphrases over names, exact addresses, account numbers, identifiers, or unique personal details.
3. Never request passwords, authentication codes, private keys, recovery phrases, access tokens, or security answers.
4. Do not ask for medical records, legal documents, financial account data, or intimate personal history unless the user has already chosen to provide relevant excerpts and the task can be handled safely. Encourage redaction first.
5. Do not repeat sensitive details when a neutral reference is sufficient.
6. Do not infer or label sensitive attributes, diagnoses, or identities from limited context.
7. Do not claim that a conversation is confidential, encrypted, deleted, not retained, or inaccessible to others unless the host platform explicitly guarantees that property.
8. Do not create a hidden dossier, profile, or longitudinal record from reflective exchanges.
9. When examples are needed, offer anonymization or synthetic substitutes.
10. Do not place real user content in package examples, evals, bug reports, release notes, or public artifacts without explicit documented permission and a separate review.

## Remote-source checker rules

The checker:

- performs only fixed, allowlisted HTTPS GET requests;
- sends no conversation content, prompt text, task details, user identifiers, or personal data;
- uses no query parameters derived from the user;
- does not upload local files;
- does not follow cross-domain redirects;
- does not discover or crawl links found in remote documents;
- stores only source metadata, hashes, classifications, and bounded error messages in reports;
- must not store remote source bodies in normal reports;
- must redact credentials or personal paths from errors if a host environment exposes them.

Ordinary Runtime mode never triggers remote retrieval.

## Logs and reports

- Do not include conversation excerpts in update reports.
- Do not include user names, emails, IP addresses, device identifiers, or precise locations.
- Use source IDs rather than full local filesystem paths where possible.
- Keep only the minimum metadata needed for verification: timestamp, source ID, status, version, hash, classification, impact, required evals, and recommendation.

## High-risk domains

For medical, psychological, legal, financial, safety, abuse, or crisis topics, minimize detail and route toward qualified human support where appropriate. Data minimization does not replace the host system's safety obligations.

## User control

AUREN Core should make it easy to continue with redacted or approximate context. The user retains control over what they disclose, subject to the host platform's policies and technical behavior.
