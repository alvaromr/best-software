# Architecture and design

**Goal:** change is cheap and local. A new feature touches one place, a rule lives in one place, and any part can be
tested in isolation. This serves changeability and correctness.

## Practices

### Boundaries
- **Keep the core pure.** Domain logic has no I/O, framework, UI or vendor types. Adapters live at the edges and
  dependencies point inward (clean / hexagonal). *Why:* a pure core is tested in milliseconds without fakes, and it
  survives a change of UI, framework or infrastructure.
- **Enforce the layering mechanically**, with an architecture test or forbidden-import rule in the gate. *Why:* a
  boundary kept only in prose erodes one "just this once" at a time.
- **Each layer calls only the one below it.** Entry points (controllers, routers, ViewModels, CLI commands) parse input,
  delegate and map results. *Why:* business rules in entry points get duplicated per entry point and cannot be tested
  without the framework.
- **Errors cross layers as domain errors.** Only the outermost layer translates them to protocol terms: HTTP status,
  exit code, UI message. *Why:* the core stays reusable across protocols, and the protocol mapping lives in one place.
- **Wrap every third-party library behind an in-project adapter or theme layer.** Callers see project or standard types
  only, enforced by forbidden-import rules. *Why:* an upgrade or replacement then touches one file instead of the whole
  codebase.
- **Route each cross-cutting concern through one chokepoint:** auth, serialization, logging, error mapping, and costly or
  sensitive calls such as paid APIs and LLMs. Add a test that fails if a new call site bypasses it. *Why:* a policy
  applied at N call sites is eventually missed at the N+1th.
- **Reach each datum through one path:** the repository. Helpers depend on the repository, never on its data sources.
  *Why:* parallel accessors drift in caching, mapping and validation, and then disagree.
- **Write to the system of record first.** Derived stores (caches, indexes) come second, and can always be rebuilt
  from it. A derived-store failure marks the derived data stale; it never reverts the record. *Why:* the record is the
  truth, and derived data is a performance detail.

### Cohesion and coupling
- **Group by feature or responsibility, not by technical kind,** once a project has more than one feature. *Why:* a
  change usually spans one feature, so its files should sit together.
- **Colocate collaborators.** A shared helper lives with the concept that owns it, not next to its first caller.
  *Why:* the next reader looks for it by concept.
- **Split a file when it holds more than one responsibility.** *Why:* mixed concepts make every change risk the other
  concept. Size is only the symptom.
- **Extend by registration:** registries, listeners and providers. A new feature is a new module plus one registration
  line, and feature modules never import each other. *Why:* the core stays closed to modification (open–closed), and
  features stay independently removable.
- **Inject dependencies through the constructor,** non-nullable. When "nothing" is valid, use a Null Object. Break a
  dependency cycle with a lazy provider, never by tolerating it. *Why:* explicit dependencies are visible, testable and
  impossible to forget to initialise.
- **Add an interface only for more than one implementation or a real test seam.** Give its members defaults so
  implementors override only what differs. Keep sensitive or environment-specific values abstract, so every
  implementor must set them. *Why:* a speculative interface is indirection with no payoff (simplicity), while a
  forgotten sensitive value is a defect (safety).
- **Integrate third parties through function-typed contracts or callbacks**, not by making them depend on your
  artifact. *Why:* coupling across organisations is the most expensive kind to undo.
- **A constant belongs to the layer that makes the decision.** *Why:* the dependency direction stays inward, and the
  decision has one owner.

### State and data flow
- **Use unidirectional data flow:** state, event, effect. Handlers take the values they need from the event, never by
  reading state back. *Why:* reading state back creates hidden ordering bugs that tests rarely catch.
- **Keep state immutable;** produce new values. *Why:* shared mutation makes behaviour depend on who touched what last.
- **Keep loading out of constructors and `init` blocks.** Key each load by the entity it loads. *Why:* construction
  stays side-effect-free, and multiple instances do not collide.
- **Keep render and pure paths free of side effects.** Do the work outside them and re-render on completion. *Why:*
  render paths run often and unpredictably.
- **Handle concurrency deliberately:**
  - Cancel in-flight work and drop stale responses when context changes.
  - Reads stay cancellable; only mutations are protected from cancellation.
  - Never block an event loop or the main thread.

  *Why:* stale responses overwrite fresh state, and blocking stalls every other request.

### Contracts
- **Prefer the simplest contract.** Use no boolean flag that switches behaviour, and let one discriminator decide.
  Required inputs are mandatory. *Why:* every flag doubles the behaviours to test, and an optional "required" input is
  a defect waiting for a caller.
- **Separate data from presentation.** Producers emit structured data and a fixed template renders it, with nothing
  hardcoded. *Why:* the data becomes testable, and the presentation becomes swappable.
- **Per-variant or per-tenant configuration lives in configuration,** never in code branches. The fallback is explicit
  and is read through one accessor. *Why:* adding a variant becomes a data change, not a code change.
- **Take facts from the authoritative source:** the compiler, the build tool, the registry, the producer's code.
  Read the producer's code at the version each environment actually runs, and confirm configuration-dependent
  behaviour in a real environment, across more than one tenant when it varies per tenant. *Why:* ad-hoc parsing and
  untrusted specs are second-hand truth that drifts, and environments can run different code and configuration.

### Libraries and SDKs
- **Expose a small explicit public surface:** internal by default, and explicit-API mode where available. *Why:*
  everything public is a promise you must keep, and an attack surface.
- **Hide transport details from consumers.** A consumer never sees status codes, JSON or endpoints, only domain types
  and domain errors. *Why:* the transport can change without breaking consumers.
- **Evolve compatibly:** add defaults, deprecate before you remove, and mark breaking changes. Check that independently
  published modules still work. *Why:* consumers upgrade on their schedule, not yours.
- **A wrapper stays a wrapper;** application logic belongs to the consumer. *Why:* YAGNI, and logic in a wrapper is
  imposed on every consumer.

### Change safety
- **Put a new behaviour that alters existing UX behind a flag.** `false` must be identical to the old behaviour. Prune
  flags that are constant everywhere. *Why:* rollout becomes reversible, while dead flags are pure complexity.
- **Fail loudly on broken invariants.** Degrade gracefully only when an *optional* capability is missing, saying why
  and how to fix it. *Why:* continuing past a broken invariant produces wrong results; a missing extra only produces
  fewer.
- **Build nothing speculative:** no infrastructure without a current consumer, no fallback paths "just in case".
  *Why:* unused code still costs reading, testing and securing, and it rots unseen.
- **When porting legacy, migrate behaviour, not code.** Pin the behaviour with characterization tests first. *Why:*
  copying code copies its defects. Tests pin what must survive, and leave the design free.

## Judgment
- Scale the number of layers to the problem. A 300-line CLI needs one pure core module and a thin entry point, not a
  DI framework.
- Some rules never relax at any size: core free of I/O, one source of truth, testable seams at external boundaries.
- Inside frozen legacy that will not evolve, make surgical changes only, and record the exception.

## Audit signals
- Domain files import framework, HTTP, database or UI packages.
- Business rules appear in controllers, ViewModels, templates or entities.
- Two code paths read or write the same datum.
- Adding a feature means editing a central `when`/`switch`.
- Vendor types appear in public signatures.
- An interface has one implementation and no test seam.
- A boolean parameter changes behaviour.
- Values are hardcoded where configuration belongs.
