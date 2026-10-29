# Documentation

**Goal:** every fact has exactly one home, is true, and is found where its reader looks for it. Nothing important lives
only in a chat or in someone's head. This serves truth and coherence, and the changeability that depends on them.

## Practices

### Single source of truth
- **State each fact once, in its canonical place, and point to it** from everywhere else. A cross-reference is a bare
  pointer, never a preview or a paraphrase. *Why:* every copy must be updated on every change, and some never are.
  Paraphrases also couple documents.
- **Docs explain why; they never transcribe** code, config values, field lists or volatile numbers such as counts,
  versions and ports. *Why:* the code already says what. A transcription is a second copy that starts to lie at the
  next commit.
- **Let decisions live in data or config** when the code reads them, with the docs referencing them. *Why:* the
  executable copy is the one that is always current.
- **Keep generated reference docs in sync with the code, enforced by a test.** Fix the docs, never the code, to match.
  *Why:* drift becomes a red gate instead of a surprise.
- **Enforce docstring rules by machine.** The linter checks the convention (for example, Google style). A test checks
  the project's own rules, such as a fixed phrasing for recurring parameters or no transport details. *Why:* docstring
  rules kept only in prose drift with every new method, while a red gate catches the first deviation.
- **When the API consumer is an LLM agent, the docstring is the tool definition.** It must say:
  - when to call the operation
  - each failure case in domain terms, and the exception it raises
  - nothing tied to one domain, app or framework
  - recurring parameters (tokens, ids) in one fixed phrasing

  *Why:* the agent has nothing but the docstring to decide with. Every gap becomes a wrong call it can only discover
  by failing.

### Layers by reader

| Reader | Home | Content |
|---|---|---|
| newcomer / user | `README.md` | what it is, install, run, test, where to read next |
| contributor / agent | `AGENTS.md` | commands, gate, architecture map, non-negotiables with their why, deviations |
| maintainer | `docs/architecture/`, ADRs | why it is built this way, rejected alternatives, measured results |
| operator | `docs/runbooks/` | deploy, rollback, rebuild from scratch, secrets backup, recovery — runnable by hand |
| API consumer | docstrings, central "Errors" section | the contract in consumer terms, no transport details |
| CLI user | `--help` | usage; others point to it |
| release reader | `CHANGELOG.md` | user-facing changes per version |
| domain newcomer | `docs/glossary.md` | the ubiquitous language, for domain-heavy projects |

*Why this split:* each reader finds what they need without wading through what they don't, and each fact still has one
home.

### Content rules
- **Docs are part of the change:** update them in the same commit, and review them before every commit. *Why:* "update
  the docs later" means never (coherence).
- **Write only verified facts.** Cite external facts with source and date, and label hypotheses. *Why:* readers act on
  docs, and a confident falsehood does more harm than a gap.
- **Record negative results and dead ends:** what was tried, why it failed, the numbers. Put a short summary at the top.
  *Why:* nobody repeats the analysis, and nobody retries the approach that already failed.
- **Record non-obvious invariants** next to the code or in AGENTS.md. *Why:* each one cost a regression once, and an
  unrecorded one will cost it again.
- **Record known limitations and deferred ideas** in the repo. *Why:* chat history is not a project memory.
- **Generalize:** write the rule a case reveals, folded into the existing structure, without dated anecdotes, ticket
  names or tool names in agent-agnostic docs. *Why:* a rule teaches every future case, while an anecdote teaches one.
- **Keep docs short and telegraphic** without losing information. Leave out what a thing does not do. *Why:* long docs
  are skimmed, and the important line gets missed.
- **Use plain language:**
  - one term per concept
  - condition first
  - imperative steps with an explicit actor
  - exact values and absolute dates
  - no jargon for external readers

  *Why:* ambiguity in instructions becomes divergence in execution.
- **Fix the output format of checklists and reports.** *Why:* the same sections every run make runs comparable.
- **Use diagrams as code (Mermaid).** *Why:* they are versioned, diffable and reviewable with the change.
- **External documents leak nothing internal,** state only what the reader needs, and have every link checked. *Why:*
  internal details are a security and confidentiality risk, and noise for the reader.
- **Explain domain jargon in the UI** for non-experts, with help kept in sync with the features. *Why:* help that the
  UI contradicts is worse than none.
- **Before a commit or release, review coherence:** does anything lie, contradict another part, or describe what no
  longer exists? *Why:* hard constraint 4. Incoherence compounds silently.

## Judgment
- A small tool may need only README and AGENTS.md. Add `docs/` when there is a decision, an operation or a limitation
  worth keeping.
- Write ADRs for decisions that are expensive to reverse or likely to be questioned. Skip them for the obvious.

## Audit signals
- The same instruction in two docs.
- Docs quoting config values.
- Stale commands, ports or versions.
- A README without install, run and test.
- Knowledge found only in chat or on a server.
- No record of rejected alternatives.
- Mixed-language docs.
- Broken links.
