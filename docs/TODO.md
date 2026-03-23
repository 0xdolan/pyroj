# Pyroj Backlog (Rebuilt)

This is the current actionable task list after the refactor and cleanup.

## P0 — Must Do Next

- [x] **Input validation hardening**
  - [x] Reject `bool` values where `int` is expected in all public APIs.
  - [x] Add explicit range checks for `month`/`day` in conversion helpers, not only in `KurdishDate`.
  - [x] Add year bounds policy and enforce it consistently.
  - [x] Raise `PyrojValueError` / `PyrojRangeError` consistently (avoid plain `ValueError` in public paths).

- [x] **Exception consistency**
  - [x] Replace `ValueError` in `pyroj/_core/convert.py` with project exceptions where exposed.
  - [ ] Add API docs section listing exact exception types per public function.

- [x] **Recreate structured roadmap artifact**
  - [x] Keep this file as source-of-truth backlog.
  - [x] Optionally regenerate a machine-readable task JSON from this file.

## P1 — High Value

- [ ] **`datetime` support parity**
  - [ ] Add `from_jdn` / `to_jdn` public APIs.
  - [ ] Add fractional JDN + time-of-day conversion methods.
  - [ ] Introduce `KurdishDateTime` wrapper (or equivalent bridge helpers).

- [ ] **Era completeness**
  - [ ] Add explicit Nineveh/612 BCE era implementation behind `KurdishEra`.
  - [ ] Add tests to prevent accidental mixing between eras.

- [ ] **Rojjmer migration closure**
  - [ ] Deprecate class-level `Rojjmer` entry point with clear warning.
  - [ ] Document removal version and migration path.

## P2 — Quality and Ops

- [ ] **Logging implementation**
  - [ ] Add module loggers (`logging.getLogger(__name__)`) in core modules.
  - [ ] Add opt-in debug mode (`PYROJ_DEBUG`) without leaking sensitive info.

- [ ] **Testing expansion**
  - [ ] Add property tests for round-trip invariants (`gregorian -> jdn -> gregorian`, etc.).
  - [ ] Add edge-case tests (leap boundaries, lower/upper year bounds, invalid type inputs).
  - [ ] Add locale JSON schema validation test for startup safety.

- [ ] **CI hardening**
  - [ ] Add coverage reporting and threshold gate.
  - [ ] Add security lint step (Bandit or stricter Ruff rules).

- [ ] **Release docs**
  - [ ] Add `CHANGELOG.md`.
  - [ ] Add migration guide section in README (`0.x -> 1.x/1.2+`).

- [ ] **Naming conventions and typing audit**
  - [ ] Audit all modules for modern PEP 8 naming consistency.
  - [ ] Ensure all public functions/methods have explicit typed signatures and typed returns.
  - [ ] Add/strengthen `TypedDict`/dataclass/Enum usage where structure is currently implicit.
  - [ ] Add typing-focused tests/checks for edge input types and overload behavior.

## Already Done (Do Not Repeat)

- [x] Runtime is stdlib-only.
- [x] Core Gregorian/Persian/Islamic conversion implemented.
- [x] `KurdishDate` core type added.
- [x] Locale catalog moved to JSON (`pyroj/locales/catalog.json`).
- [x] Safe fixed-token formatting API added.
- [x] Basic CI (pytest/ruff/mypy) added.

## Things We Still Have Not Explicitly Considered

- **Calendar model policy:** tabular Islamic vs observational moon-sighting differences should be explicit in API docs and naming.
- **Backwards compatibility matrix:** define which legacy outputs are guaranteed bit-for-bit compatible with old pyroj.
- **Data governance for locales:** decide review process for locale spelling changes (source references, reviewer approval).
- **Versioning policy:** codify SemVer rules for calendar behavior changes (these can be breaking even if signatures stay same).
- **Performance and precision envelope:** define tested year range and precision guarantees for JDN floating operations.

## If I Were Improving It Further

- Split `_core/convert.py` into smaller modules (`gregorian.py`, `persian.py`, `islamic.py`, `jdn.py`) to reduce coupling and improve test focus.
- Add a strict `typing` layer for user input coercion/validation, and keep core math functions pure and internal.
- Add a small benchmark suite and lock expected performance for typical conversion workloads.
- Add a schema + checksum step for `catalog.json` so accidental edits fail fast in CI.
- Add examples for each locale and each calendar in README with expected outputs for one canonical date.
