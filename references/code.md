# Code: naming, readability, types, errors

**Goal:** a stranger reads any file once and knows what it does and why. The compiler rejects illegal states, and no
failure goes unnoticed. This serves changeability, correctness and truth.

## Practices

### Naming and language
- **Name things for what they are or do.**
  - Use no vague role words: `Manager`, `Helper`, `Util`, `data`, `info`, `temp`, `result`.
  - Functions start with a verb; booleans read `is`, `has`, `can` or `should`.
  - Enforce it with a forbidden-name lint where available.

  *Why:* a name is the most-read documentation, and vague names hide mixed responsibilities.
- **Use one term per concept** across code, docs and UI. Avoid names that collide with another concept or library.
  *Why:* synonyms make readers wonder whether two things differ.
- **Rename as soon as a name lies.** Sweep every leftover, and check that the target name is free first. *Why:* a
  lying name is a false statement read on every visit (truth).
- **Write every professional artifact in English.** *Why:* the constitution's "Language of artifacts".
- **Key persisted data by stable identifiers,** never by display names. *Why:* display names change, and keys must not.

### Readability
- **Code explains itself; a comment is the exception.**
  - A comment explains a non-obvious *why*, such as an invariant that once cost a regression.
  - It is generic (no ticket, person or incident), truthful, and never narrates the code.
  - A rationale needed in several places is written once and referenced.
  - Remove commented-out code.

  *Why:* comments that restate code rot into lies, and the ones that survive should carry what code cannot say.
- **Template comments use the template engine's syntax.** *Why:* HTML comments reach the client and leak internals.
- **Keep functions small and cohesive:** guard clauses, flat flow. Complexity thresholds flag smells; cohesion decides.
  Never game a size rule; extract properly. *Why:* one level of abstraction per function keeps it readable, while hacks
  that dodge the metric keep the problem and hide it.
- **Use named arguments when adjacent parameters share a type** or a call has more than about three arguments. Public
  APIs are keyword-only where possible, and more than about four parameters calls for a parameter object. *Why:* a
  swapped pair of same-typed arguments compiles and fails at runtime.
- **Remove needless branches, toggles and options.** *Why:* each one multiplies the behaviours to test and explain.
- **Prefer functional, immutable code:** pure functions, `map`/`filter`/`fold` when clearer, immutable models and
  collections. *Why:* pure code is testable in isolation, and immutable data cannot change behind your back.
- **Name constants instead of magic literals,** and define each constant, string, format or presentation rule once.
  *Why:* a repeated literal is a rule stated many times, and it drifts.
- **Match the conventions already in the codebase:** "nothing the owner would not write". *Why:* consistency lets
  readers predict code, and a second style is a second dialect to learn.

### Simplicity and dead weight
- **KISS:** choose the simplest design that meets the requirement. When a fix keeps growing, stop and restart from
  options. *Why:* a growing fix signals a wrong model, and patching it compounds the error.
- **Climb the minimalism ladder before writing code:**
  1. YAGNI: should this exist at all?
  2. Reuse what the codebase already has.
  3. Use the stdlib.
  4. Use a native platform or framework feature.
  5. Use an installed dependency.
  6. Write a one-liner.
  7. Write the minimum code.

  Security, validation, error handling and accessibility are never trimmed. *Why:* the cheapest code to maintain is
  code that does not exist, but the four exceptions protect safety and correctness, which outrank simplicity.
- **Apply DRY to knowledge, not to coincidence.** Unify the same rule, constant or format. Leave apart look-alikes that
  change for different reasons. *Why:* duplicated knowledge drifts, but merging coincidences couples unrelated modules.
- **Delete dead code in the same change that kills it:** functions, parameters, imports, resources, flags. An
  unreachable branch is deleted, never excused from coverage. *Why:* dead code misleads readers about
  what the system does (truth).
- **Find the root cause; never ship a workaround or a defensive fix made blind.** *Why:* a workaround leaves the
  defect in place and adds a second thing to understand, and a guard without understanding moves the failure
  somewhere harder to see.

### Types
- **Use the strictest type checking from day one,** with warnings as errors.
  - Use no `any`, `!!`, unsafe casts or blanket ignores.
  - A justified suppression is narrow and states its reason.

  *Why:* every check the compiler does is a test you never have to write or run.
- **Make illegal states unrepresentable:**
  - Use sealed types, enums or literal unions for closed sets, matched exhaustively without `else`.
  - Use `null`/`None` for absence, never `0` or `""` as a stand-in.
  - Use value objects for domain primitives, and integers where the domain is integral.

  *Why:* states the type system rejects cannot happen in production. An `else` silently swallows the next variant.
- **Derive optionality from the real producer;** when unsure, keep the field nullable. *Why:* a spec that lies about
  nullability turns into a crash in production.

### Errors
- **Never fail silently:**
  - Never swallow an exception.
  - Catch the narrowest type you observe.
  - Use a catch-all only at the top-level boundary, with logging.
  - Never swallow cancellation.

  *Why:* a silent failure turns a visible bug into wrong data, which costs far more to find.
- **Raise specific, named domain errors,** one mechanism per kind of failure. Messages state the cause in domain terms
  and what to do, and each error is documented once. *Why:* callers can handle what they can name, and people can fix
  what the message explains.
- **Parse external input into types at the boundary,** after validating it (`security.md`, "Input and execution").
  *Why:* the inside can then trust its types.
- **Fail fast at startup on missing configuration or secrets.** *Why:* a crash at boot is cheap; an insecure default in
  production is not.
- **Guard platform calls that throw** at the call site. Surface the failure through the UI-event mechanism, then audit
  for the same pattern elsewhere. *Why:* the same mistake usually exists in more than one place.
- **Make fallback control flow explicit.** *Why:* implicit fallbacks hide which path ran.
- **Security guards fail closed,** with a named message. *Why:* a guard that allows on crash is no guard.

## Judgment
- Comment density follows the codebase's convention. A public library adds docstrings written for its consumer.
- When a linter threshold blocks a good design, raise it once, with the reason in the config. Never raise it to hide
  debt.

## Audit signals
- Vague names. `changeability`
- Mixed languages in one artifact. `changeability`
- Comments that narrate the code, or commented-out code. `changeability`
- Empty or broad catches. `correctness`
- `any`, `!!` or ignores with no reason. `correctness`
- Repeated magic numbers. `changeability`
- Duplicate helpers. `changeability`
- Unused symbols. `simplicity`
- `else` over sealed or enum types. `correctness`
