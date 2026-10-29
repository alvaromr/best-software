# UI and accessibility

**Goal:** every user, including assistive-technology users and first-time non-experts, can perceive, understand and
operate the product. The UI is consistent, resilient and localizable. This serves correctness for every user, and
safety for their data.

## Practices

### Accessibility (WCAG 2.2 AA as a requirement)
- **Use real semantics:**
  - headings and landmarks
  - merged semantics for compound items
  - labels on every control and field
  - live regions for async state
  - custom actions for complex gestures

  Screen readers read only what is visible. *Why:* assistive technology sees only the semantics. A UI without them is
  broken for those users, even when it looks fine.
- **Support the keyboard on every primary flow:** focus order, visible focus, and Escape to close. *Why:* keyboard
  users include power users, motor-impaired users and every screen-reader user.
- **Never use colour as the only signal,** ensure contrast (including over imagery and system bars), and give each
  colour one meaning. *Why:* colour-blind users and bright screens lose colour-only information, and reused colours
  confuse everyone.
- **Respect user settings:**
  - reduced motion
  - large font scales, solved by layout instead of clamped text
  - dark mode
  - resizable windows
  - no needless orientation lock

  *Why:* the user's settings express a need, and overriding them excludes the user.
- **Verify with real assistive technology plus automated checks,** treating scanner findings as claims to verify, and
  gate UI commits where tooling allows. *Why:* scanners miss most real barriers and also report false ones.

### Design system
- **Keep design tokens in one place;** restyle by editing tokens only. *Why:* one source of truth for visual decisions
  keeps screens coherent.
- **Wrap UI libraries in themed components;** feature code never imports raw widgets (forbidden-import rule). *Why:*
  consistency by construction, and a library swap in one place.
- **Pass behaviour through composition slots or explicit parameters,** not hidden global context. *Why:* implicit
  context makes components unpredictable and hard to test.
- **Reusable components take a `modifier`/`className` applied to the root,** follow the platform's parameter order, and
  keep previews private and working. *Why:* callers control layout predictably, and broken previews hide regressions.

### Content and i18n
- **Keep user-visible strings in resources once a second language is supported or planned,** translated into every
  supported language and formatted through one helper. Until then:
  - keep each module's strings together
  - never build sentences from fragments
  - format through one helper

  *Why:* resource files for a single language are speculative indirection. Keeping the strings together and whole
  makes a later extraction mechanical, and that removes the costly retrofit the rule exists to avoid.
- **Write for the audience:** plain language, little jargon, and contextual help kept in sync with the features. *Why:*
  a user who does not understand an option cannot use it safely.

### States and resilience
- **Design and test every state:** loading, empty, error, partial, many, overlapping, offline. *Why:* the happy path is
  the minority of real sessions.
- **Show errors with a retry;** never substitute silent defaults that could overwrite user data. *Why:* a silent
  fallback that saves defaults destroys real data. Hard constraint 2.
- **State survives configuration changes and process death,** keeps the user's place, and initial loads do not re-fire
  on recreation. *Why:* rotation, low memory and backgrounding are normal, not edge cases.
- **Validate on submit and say what is expected;** keep text selectable. *Why:* users can fix only what they understand.

### Verification
- **Verify UI changes in the real app or browser,** at target sizes, with before and after captures, across every
  variant that reaches the screen. Test sizes with your own window, an iframe or DevTools, never by resizing the user's
  window. *Why:* rendering is where reading the code stops being reliable.
- **Ship no speculative UI infrastructure,** and do not polish screens about to be replaced. *Why:* simplicity, and
  effort is better spent on what users will see.

## Judgment
- A CLI's UI is its output and `--help`: clear errors, exit codes, `--json` for machines, colour off when not a TTY.
- Internal tools still meet keyboard and contrast basics. Full assistive-technology verification scales with audience.

## Audit signals
- Unlabeled controls.
- No keyboard path.
- Colour-only state.
- Clamped font scaling.
- Hardcoded colours, scattered strings, or sentences built from fragments.
- Raw library widgets in feature code.
- No empty or error states.
- A locked orientation.
- Silent fallbacks on error.
