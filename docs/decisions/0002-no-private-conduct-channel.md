# No private channel for conduct reports

- **Date:** 2026-11-20
- **Decided by:** the owner
- **Practice set aside:** a code of conduct names a contact for reports (the Contributor Covenant's enforcement
  section).

## Context
The repo takes outside contributions, so it has a code of conduct (`references/repository.md`, root files). GitHub
offers no private channel from a reporter to the owner: the account's address is a `noreply` one, there are no
private messages, and private vulnerability reporting takes security reports only. The owner's main personal address
is never published (`references/security.md`, "Reporting channel").

## Why the value is not at stake
The contact protects reporters' safety: a report about a person needs a place to go. With almost no contributors
yet, GitHub's "Report content" covers abuse on the platform, and an issue covers a report that can be public, so a
reporter still has somewhere to go, and the code of conduct says so.

## Rejected alternatives
- A forwarding alias kept only for conduct reports. Revisit when the project has regular outside contributors.
- Private vulnerability reporting for conduct reports: reporters would not expect it, and each report would be
  recorded as a security advisory.
