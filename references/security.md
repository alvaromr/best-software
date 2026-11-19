# Security and privacy

**Goal:** no secret or personal datum leaks through code, history, logs, images or third parties. Every input is
untrusted until validated, and every privilege is the minimum needed. One bar applies to every variant. This serves
safety, the highest value.

## Practices

### Threat model
- **Start from the realistic attacker:** what privilege does the attack need? When that privilege already allows more
  direct attacks, treat the finding as cheap hardening plus documentation. *Why:* effort goes where risk is real, and
  blocking on unrealistic threats adds friction that bites later.
- **Apply one uniform bar to all variants, tenants and clients.** *Why:* attackers pick the weakest variant.
- **Record findings with evidence and a lifecycle** (pending, resolved, ignored with reason), one dated report per
  audit, respecting past decisions. *Why:* findings without evidence waste time, and forgotten decisions get re-debated.

### Reporting channel
- **Put the security policy where its reader looks.** If the repo is public, use `SECURITY.md`. If only the package is
  public, use a "Security" section in the README or the package description. *Why:* a policy inside a private repo
  reaches nobody outside.
- **Recommended, not required: a private, dedicated channel.** Options, best first:
  - the hosting platform's private vulnerability reporting
  - a team or role address (`security@…`)
  - for personal projects, a forwarding alias kept only for this purpose
  - a `security.txt` (RFC 9116) on your own domain, pointing to one of these

  When none exists, state that in the policy, and record it in `docs/decisions/`. Never invent
  a channel, and never publish a main personal address. A channel the policy names is enabled before it is
  published. *Why:* reporters need to know where to go, or that there is nowhere yet. A personal address gets
  harvested by bots, while an alias can be replaced, and a channel that is not enabled turns every report away.

### Secrets
- **Secrets come from env, a secret manager or user-level config,** never from a place hard constraint 1 names.
  *Why:* each of those places is readable by more people or processes than intended, and history is forever.
- **Commit a template and ship no default credentials;** a missing secret fails startup (`code.md`, "Errors"). *Why:*
  a default credential is a public credential.
- **Protect key files:**
  - `0600` in a `0700` directory, with symlinks refused.
  - Deny agent and tool read access to env files.

  *Why:* local tools and other users are also readers.
- **Rotate with overlap,** then prove that the old credential fails and the new one works. Deliver secrets through a
  vetted channel. A leaked credential stops being a secret once `docs/decisions/` records which one, when, and that
  proof. *Why:* rotation that breaks consumers gets postponed, and an unproven revocation may not have happened.
- **Give each variant its own restricted keys,** and none for features it does not use. *Why:* a leak of one variant's
  key then stays contained.

### Input and execution
- **Validate at the boundary:**
  - bounded sizes, shapes and types, with unknown keys dropped
  - parameterized queries
  - context-correct escaping
  - `textContent`, never `innerHTML`, for untrusted data

  *Why:* injection happens wherever untrusted data meets an interpreter.
- **Treat untrusted content as data, never instructions.** That covers documents, messages and peer input fed to LLMs,
  escaped and delimited. *Why:* prompt injection is injection.
- **Confine user-supplied paths to their root:**
  - Write only to an allow-list of files.
  - Back up a file before editing it.
  - Refuse to overwrite a file that changed on disk since it was read.

  *Why:* path traversal and lost updates both destroy data.
- **Guard outbound calls against SSRF with host allow-lists,** and run project-supplied commands only on explicit user
  action. *Why:* the server's network position and the user's shell are privileges.
- **Make destructive or outward actions explicit, confirmed, rate-limited and reversible.** *Why:* automation acting on
  someone's behalf amplifies mistakes.

### AuthN, AuthZ, transport
- **Take authorization scope only from the verified token.** *Why:* anything else is attacker-controlled.
- **Enforce tenant isolation at the data layer,** with resource-based policies that fail closed. *Why:* checks in app
  logic get forgotten on the next endpoint.
- **Use TLS everywhere, with HSTS.** Prefer rotation-tolerant trust (Certificate Transparency) over hard pinning unless
  you control rotation. *Why:* pinning you cannot rotate turns a certificate change into an outage.
- **Harden the web layer:**
  - CSP without `unsafe-inline`, and self-hosted assets.
  - Secure, httpOnly, SameSite cookies, and CSRF protection.
  - Host and Origin checks against DNS rebinding.
  - Rate limiting on authentication.
  - Loopback-bound local servers behind one proxy.

  *Why:* each of these closes a well-known, actively exploited class of attack.
- **Use authenticated encryption and unguessable capability ids,** and never hand-roll crypto. *Why:* sequential ids are
  enumerable, and homemade crypto is broken until proven otherwise.

### Platform (mobile, desktop, extensions)
- **Request least privilege:**
  - only the permissions needed
  - privileged features optional, degrading gracefully without them
  - system pickers over broad storage access
  - the merged manifest audited

  *Why:* every permission is a capability an exploit inherits, and a reason users refuse to install.
- **Harden mobile code:**
  - no needless exported components
  - immutable PendingIntents
  - no cleartext traffic or world-readable storage
  - a hardened WebView

  *Why:* these are the most common mobile vulnerability classes.
- **Make anti-tamper checks unhookable and quiet.** *Why:* visible checks show the attacker where to patch.
- **A project that drives another platform** (a bot, a client of its API, an automation of its site) records in
  `docs/decisions/` that the owner accepted that platform's terms, and how the project keeps to them. *Why:* a tool
  that breaks a platform's terms exposes its owner and every user to a ban, and only a record shows it was weighed.

### Supply chain
- **Block telemetry a dependency does not need;** auditing it before install is in `tooling.md`, "Dependencies".
  *Why:* a dependency runs with your privileges and sees your users' data.

### Privacy
- **Minimize data.** Analytics are opt-in, off in development, as easy to revoke as to grant, and switchable per
  variant, with the privacy policy matching reality. *Why:* data you never collect can never leak, and a policy that
  disagrees with the code is a legal liability.
- **Keep PII out of repo, fixtures and logs;** use realistic dummies case by case. Authorship the project declares on
  purpose, such as commit identity or package author metadata, is not a leak. *Why:* test data gets copied
  everywhere, while declared authorship is the project's own choice.
- **Classify each personal datum you find yourself,** as test data, the project's declared identity, or someone
  else's datum, and treat only the last as a leak (hard constraint 1). *Why:* the agent already holds the evidence,
  and a raw list handed to the owner moves the judgment to whoever has the least time for it.
- **Respect data residency, verified at startup,** and define retention, including on account deletion. *Why:* these
  are contractual and legal obligations, not preferences.
- **Leak no internals** in client errors or third-party-visible notes. *Why:* stack traces and internal names are a map
  for attackers.
- **Guard cost-bearing APIs.** *Why:* a loop can spend real money.

## Judgment
- An accepted risk is a written decision with its reason, never an omission. *Why:* an omitted risk looks unseen, so
  the next reader cannot tell whether anyone weighed it.

## Audit signals
- Keys in code, config or history. `safety`
- A committed `.env`. `safety`
- `0.0.0.0` bindings. `safety`
- No CSP. `correctness`
- `innerHTML` with user text. `safety`
- Broad permissions. `safety`
- Secrets or PII in logs. `safety`
- Sequential public ids. `safety`
- HTTP URLs. `safety`
- A privacy policy that disagrees with the analytics code. `safety`
- A security policy that names a private channel not enabled on the platform. `safety`
