# Best software — score

Measures how far a project is from the bar, as a global score and one score per section, without changing the project.
The score is orientative: an agent assigns it, so two runs on the same commit can differ. *Why:* a number makes progress
and regressions visible over time; the history file makes each number traceable to the signals behind it.

## Rules
- **Read-only.** Change nothing in the project except the score file. Files the checks write as usual and git ignores
  (coverage, caches, build output, mutation results) are fine. If the dependencies are missing, install them from the
  lockfile alone, with the project's own package manager and no updates; if that is not possible, the checks are
  unverified.
- **The checks:** the gate (`references/tooling.md`), plus the heavy checks the project runs before push or
  integration (mutation, audits) and its documented build or package check. Never run checks against live or
  production systems: they need real credentials and act on real data (safety).
- **Cached results** count only when the tool invalidates them on every change that could alter them. Otherwise run
  the tool fresh, deleting its git-ignored output first; if a fresh run cannot finish, the result is unverified.
- **One commit.** If HEAD moves during the run, rerun the checks on the final HEAD, score that commit and say so.
- **Sections:** the references with audit signals, in this order: `architecture`, `code`, `testing`, `tooling`,
  `repository`, `docs`, `git`, `release`, `security`, `operability`, `ui`. `toolchains.md` is not scored, because a
  tool can be swapped for an equivalent.
- **Signals:** a section's signals are its reference's audit signals, plus any breach of a practice in the
  "Never scales down" column of Step 1. Other gaps go to the report as observations, unscored. *Why:* a fixed list
  keeps runs comparable.
- **One section per piece of evidence.** Score each piece of evidence once, in the section whose reference states the
  practice it breaks. If several do, use the first of them in the order above.
- **Severity is the value at stake in this instance.** Start from the value the practice protects: the one its *Why*
  names, or else the harm it describes (harm to users, data, secrets or privacy is safety; a wrong or unnoticed result
  is correctness; a stale or contradictory statement is truth; a costly or risky change is changeability; needless
  code, dependencies or options are simplicity; wasted time or resources is efficiency). Then ask whether that value
  is really at stake here (constitution, "How to decide", step 2), and lower it to the one that is. State why in the
  signal's `reason`. *Why:* a practice's worst case, applied to a harmless instance, scores noise; an unused dev
  dependency with a clean audit is a simplicity signal, not a safety one. A copied value or duplicated instruction is
  changeability when you verify that it still matches its source, and truth when it does not.
- **Recorded deviations.** A deviation recorded in the project's `docs/decisions/` is not a signal when the entry
  shows that the owner decided it, or approved an agent's proposal that names the value not at stake and why. Any
  other entry, such as an agent's unapproved one, still counts, and so does a gap listed only as pending elsewhere,
  such as a plan or TODO. *Why:* a deviation is the owner's call; an agent cannot excuse its own gaps.
- **Judge what applies.** Skip a signal when its practice's reason does not hold in this project (constitution, "How
  to decide", step 2), and give the reason; the burden of proof is on the skip. A deploy signal in a library, or a
  gate of types, tests and coverage in a repo with no executable code, is skipped; what that repo still needs, such as
  coherent docs, is judged for what it is. A practice in the "Never scales down" column never shrinks with size, only
  with the absence of its subject. A section has no score only when none of its practices applies, such as `ui` in a
  library with no interface. *Why:* an agent scores, not a script, so that each practice is weighed against the
  project it meets.
- **Unverified counts as present.** A signal that the repo, its history or the checks could show, but that could not
  be checked this run (a check did not run, a tool was missing), counts as found and is marked unverified (hard
  constraint 5; a missing gate is never a pass). A signal that no snapshot can show, such as knowledge kept only in
  chat, is skipped.
- **Hard constraints in a snapshot:** a constraint counts as broken only on direct evidence of one of these: a secret or
  personal datum in the repo, history or logs (1); a swallowed error or silent fallback (2); a moved tag or rewritten
  published history (3). The others govern how a change is made and leave no reliable trace in a snapshot, so their
  traces score by the value at stake. Authorship the project declares on purpose (commit identity, package author
  metadata) is neither a personal datum for constraint 1 nor a signal; the rule against a main personal address
  applies only to the security contact. Test data that identifies no real person is not a personal datum either. A
  leaked credential is no longer a secret once the deviations record it as revoked: which one, when, and how the old
  one was proven to fail (`references/security.md`, rotation).
- **No secret values.** Evidence is a `file:line`, a commit or a command, never the secret or personal datum itself
  (hard constraint 1).

## Scale
A section's score is set by its most severe signal:

| Most severe signal | Score |
|---|---|
| none | 10 |
| simplicity or efficiency | 8 |
| changeability | 6 |
| truth and coherence | 4 |
| correctness | 2 |
| safety, or a broken hard constraint | 0 |

The global score is the mean of the applicable sections, to one decimal. If any hard constraint is broken, the global
score is at most 4.0. *Why:* a mean alone would hide a leaked secret among nines.

## Procedure
1. **Profile the project** (Step 1).
2. **Run the checks** and record each command's result.
3. **Assess every section** under the rules above.
4. **Compare with the previous run**, if the score file has one. List each signal that appeared or disappeared, and
   its cause: a new commit, a different `skill_commit`, or, when neither changed, the agent's judgment.
5. **Write the score file** (below).
6. **Report** in the format below. A leaked secret goes first, for rotation (Step 2b).

## Score file (`.best-software-score.json`)
- **Location:** the repository root. Add `.best-software-score.json` to the file that
  `git rev-parse --git-path info/exclude` names, unless it is already there. *Why:* the score stays private and
  uncommittable without touching the project's `.gitignore`.
- **Not a git repo:** write it at the project root, with `commit` and `clean_tree` as `null`, and say that nothing
  excludes it.
- **History:** append each run to `runs`, newest last; never rewrite earlier runs.

```json
{
  "note": "Orientative: an agent assigns this score, so it can vary between runs on the same code.",
  "runs": [
    {
      "date": "<ISO 8601, UTC>",
      "commit": "<project HEAD sha>",
      "clean_tree": true,
      "skill_commit": "<this skill's HEAD sha>",
      "skill_clean_tree": true,
      "model": "<model id>",
      "profile": "<kind · stack · audience · constraints>",
      "checks": [
        { "command": "<command>", "result": "pass", "detail": "<coverage, mutation score, cached or not>" }
      ],
      "global": 6.4,
      "hard_constraints_broken": [{ "constraint": 1, "evidence": "<file:line, commit or command>" }],
      "sections": {
        "testing": {
          "score": 4,
          "worst_value": "truth",
          "signals": [
            {
              "signal": "<audit signal>",
              "value": "truth",
              "reason": "<why this value is at stake here>",
              "evidence": "<file:line, commit or command>",
              "verified": true
            }
          ]
        },
        "ui": { "score": null, "not_applicable": "<reason>" }
      },
      "observations": ["<unscored gap> — <evidence>"]
    }
  ]
}
```

`result` is `pass`, `fail` or `not_run`. Values are written as `safety`, `correctness`, `truth`, `changeability`,
`simplicity` and `efficiency`.

## Report format (in Spanish)
The main signal of a section is its most severe one. On a tie, the reference's audit signals come first, in their
list order, then the "Never scales down" rows, in table order. The cap line
appears whenever a hard constraint is broken, even if the mean is already below 4.0.

```markdown
## Nota: <global>/10
<si hay restricción dura rota: «Tope de 4,0 por la restricción dura <n>: <evidencia>»>

## Perfil
<tipo · stack · audiencia · restricciones>

| Sección | Nota | Señal principal |
|---|---|---|
| <sección> | <nota o «n/a: motivo»> | <señal> — <evidencia> |

## Observaciones
<huecos sin puntuar; omitir si no hay>

## Cambios respecto a la ejecución anterior
<señales que aparecen o desaparecen; omitir si es la primera>

Nota orientativa: la asigna un agente y puede variar entre ejecuciones.
```
