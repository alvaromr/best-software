# Observability and performance

**Goal:** when something fails in production, the data to find the cause already exists, and no secret or personal
datum is exposed. Performance decisions rest on measurements, not guesses. This serves correctness, safety and, last,
efficiency.

## Observability
- **Log through one project logger:**
  - Configure it once and write to stdout: JSON in production, readable in development.
  - Use fixed `snake_case` event names and one canonical key per concept.
  - Use UTC ISO-8601 timestamps, and levels that state intent.

  *Why:* structured, consistent logs can be queried, while ad-hoc strings can only be grepped and guessed at.
- **Correlate requests** with a `request_id` bound in middleware. Identify actors with a hashed id, and log route
  templates, not raw paths. *Why:* one request's story must be reconstructible, without logging identities or ids.
- **Log each event once, in the layer that owns it,** never duplicated or truncated misleadingly. *Why:* duplicate and
  half lines mislead whoever debugs next.
- **Redact by key,** case-insensitive and recursive, and test it. Log names, not contents. Release logs carry keys,
  not values. *Why:* logs are copied to many places and kept long, which makes them the classic leak.
- **A library logs only on its own named logger.** It never adds handlers to, or changes the level of, loggers it
  does not own, its dependencies' included. *Why:* logging configuration belongs to the application, and a library that
  touches it silently changes the logging of the code around it.
- **Surface failures to the user or operator with their cause;** never fail silently. *Why:* hard constraint 2. An
  invisible failure cannot be fixed.
- **Report crashes with breadcrumbs, and triage every issue:**
  1. Download the complete data, paginated.
  2. Assign ownership with evidence.
  3. Close it with a note and the fixing version.
  4. Mute unactionable issues, with the reason.

  *Why:* an untriaged crash list becomes noise, and the real regressions drown in it.
- **Instrument before guessing:** add diagnostics, wait for data, then fix. Remove temporary diagnostics before commit.
  *Why:* fixes based on assumed causes often fix nothing.
- **Verify telemetry really arrives** at the backend, past the CSP. *Why:* a dashboard at zero looks the same as no
  traffic.
- **Expose health and readiness endpoints,** and provide log-query tasks runnable from the developer machine. *Why:*
  operations should not require installing tools on servers or remembering queries.
- **Build debug tooling into the product, kept out of release:**
  - state export and import
  - scenario loaders
  - overlays that explain decisions
  - a performance meter
  - a debug aid with each new mechanic

  *Why:* the hardest bugs are the ones you cannot reproduce, and replayable state makes them reproducible.

## Performance
- **Measure before optimizing:** run an A/B with real tools and record the numbers. Reject marginal wins that add risk,
  and revert what does not pay off. *Why:* efficiency ranks below simplicity unless measurement proves it matters.
- **Bound the work per frame or per request,** with the cheapest check first. *Why:* one pathological case must not
  freeze everything.
- **Never block the event loop or main thread, and cancel stale work.** *Why:* one blocking call stalls every user.
- **Kill N+1 queries,** and push filtering and sorting to the datastore. *Why:* per-item queries scale with the data,
  which is how they explode.
- **Compute derived data once and cache it,** keyed by version or mtime, with explicit invalidation. *Why:* a cache
  without a key or invalidation serves stale data (truth).
- **Respect upstream systems:** polling caps, backoff, explicit single-process assumptions. *Why:* your client must not
  be the incident in someone else's system.
- **Design for the weakest target machine or device,** with adaptive polling and pause when idle. *Why:* users do not
  all have your laptop, and battery is a feature.
- **Ship lean assets:**
  - Compile CSS at build time.
  - Compress images.
  - Serve static files from the proxy.
  - Preload what decides layout.

  *Why:* bytes cost load time on every visit.
- **Keep the build fast:** cache, parallel, incremental, and verify with the narrowest target. *Why:* a slow build
  lengthens every feedback loop.
- **Avoid needless re-rendering and reloads:** keyed effects, stable lambdas, and no full reload after one write. *Why:*
  wasted work shows up as jank and battery drain.

## Judgment
- Logging depth scales with deployment: a CLI logs to stderr at levels, while a service adds structure, correlation and
  health.
- A performance requirement needs a number and a measurement method before it justifies complexity.

## Audit signals
- `print` logging. `changeability`
- Duplicate or truncated logs. `correctness`
- Secrets or PII in logs. `safety`
- No correlation id. `changeability`
- Silent failures. `correctness`
- No health endpoint. `correctness`
- Optimizations without numbers. `simplicity`
- Blocking calls in async code. `efficiency`
- Unbounded per-frame or per-request work. `efficiency`
- Queries inside loops. `efficiency`
