# Remediation Plan — Security, Design Standards, and TaskMaster Alignment

This document reviews `docs/REFACTOR_TASKMASTER.json` against the current implementation, `docs/ARCHITECTURE.md`, and `SECURITY.md`, then lists gaps and a prioritized remediation path **before** marking the refactor “fully done.”

---

## 1. TaskMaster status vs. reality

The JSON file still marks **all** tasks `T1`–`T10` as `"status": "pending"`. The repository has **partial implementation**; the task file is **out of sync** with the codebase.

| Task | Subtasks | Implementation status (code review) | Notes |
|------|----------|-------------------------------------|--------|
| **T1** Packaging | T1.1–T1.3 | **Largely done** | `pyproject.toml` exists; `setup.py` removed (not deprecated as thin shim); README states Python 3.10+. **T1.2** is “removed,” not “shim” — update task text or add optional `setup.py` shim for legacy `pip install` workflows. |
| **T2** JDN / Gregorian | T2.1–T2.3 | **Partial** | `gregorian_to_jdn` / `jdn_to_gregorian` + golden tests exist. **T2.2** fractional day / `datetime` integration **not** implemented. **T2.3** full parity with TS `gregorian.spec.ts` (formatting, TZ) **not** done (stdlib-only date-only scope). |
| **T3** Persian | T3.1–T3.3 | **Core done** | Leap, month lengths, tests; **T3.3** broader TS Persian tests not fully ported. |
| **T4** Islamic | T4.1–T4.2 | **Core done** | Tabular Islamic; **T4.2** full TS islamic suite not fully ported. |
| **T5** KurdishDate / era | T5.1–T5.4 | **Partial** | `KurdishDate`, `KurdishEra.SOLAR_PERSIAN_OFFSET` only. **T5.3** explicit Nineveh-era docs/API **missing**. **T5.4** Kurdish TS tests not fully ported. |
| **T6** Locales | All | **Not done** | No `locales/` registry, no safe formatter. |
| **T7** Exceptions / logging | T7.1–T7.2 | **Partial** | `PyrojValueError` / `PyrojRangeError` exist. **No** module logging, **no** `PYROJ_DEBUG`, **no** structured log policy in code. |
| **T8** Documentation | T8.1–T8.3 | **Partial** | README quickstart exists; **CHANGELOG** and migration guide **missing**; docstring coverage incomplete vs. NumPy/Google style everywhere. |
| **T9** CI / pre-commit | T9.1–T9.2 | **Not done** | No GitHub Actions workflow; no `.pre-commit-config.yaml`. |
| **T10** Rojjmer deprecation | T10.1–T10.2 | **Partial** | `DeprecationWarning` on `to_kurdish(solar=True)` only; **`Rojjmer` class itself not deprecated**; no published removal version/schedule. |

**Remediation (process):** Update `REFACTOR_TASKMASTER.json` (or regenerate from Task Master AI) so **status** and **subtasks** reflect the table above, or add a `meta.last_reviewed` field and automation rule to sync on each release.

---

## 2. Security and robustness gaps

Aligned with `SECURITY.md` (no secrets, no `eval`/`pickle`, validation, safe formatting).

### 2.1 Input validation and “sanitization”

For a pure calendar library, “sanitization” means **strict type and range checks** on all public entry points, predictable exceptions, and **no** silent coercion of invalid inputs.

| Gap | Risk | Severity |
|-----|------|----------|
| `pyroj._core.convert.gregorian_to_jdn`, `jdn_to_gregorian`, `persian_to_jdn`, `jdn_to_persian`, `islamic_to_jdn`, `jdn_to_islamic` accept **int-like** values without validating **month 1–12**, **day** within calendar rules, or **year** within documented bounds. Out-of-range values can yield **nonsense dates** or rely on `datetime.date` failing later. | Wrong results; harder debugging; possible edge-case instability with extreme values. | **Medium** |
| `persian_days_in_month` raises built-in **`ValueError`** for bad month; architecture and `KurdishDate` use **`PyrojRangeError`**. Inconsistent exception type breaks callers that catch `Pyroj*` only. | API contract inconsistency. | **Low–Medium** |
| **`bool` is a subclass of `int`** in Python: `KurdishDate(..., True, ...)` can be accepted where `month`/`day` are expected, masking bugs. | Subtle logic errors in callers. | **Low** |
| `float` / `NaN` / `inf` passed where `int` is expected: Python may coerce or propagate **NaN** through JDN math; behavior is undefined. | Rare but hard-to-debug failures. | **Low** |
| No documented **supported year range** (proleptic Gregorian / Persian / Islamic). Extreme values may cause performance issues or float precision issues. | Availability / correctness. | **Low** |

### 2.2 Logging and observability

| Gap | Risk | Severity |
|-----|------|----------|
| `ARCHITECTURE.md` / **T7** require module loggers and optional debug; **no `logging` usage** in `pyroj` sources. | Harder operational diagnosis; no structured hook for `PYROJ_DEBUG`. | **Low** (for a small lib) |

### 2.3 Future features (T6 / formatters)

| Gap | Risk | Severity |
|-----|------|----------|
| **T6.4** “safe strftime-like formatter” **not implemented**. If added later without discipline, **user-controlled format strings** can become injection or DoS vectors (regex blowup, accidental `%` formatting). | **High** *when implemented*; currently N/A. | **N/A** now |

### 2.4 Supply chain and delivery

| Gap | Risk | Severity |
|-----|------|----------|
| **T9** missing: no CI (pytest, ruff, mypy) on every push/PR. | Regressions and insecure patterns slip in. | **Medium** |
| Dev dependencies not pinned in a **lock file** (optional but modern practice). | Reproducible builds. | **Low** |

---

## 3. Design and modern-pattern gaps

| Gap | Standard / pattern |
|-----|-------------------|
| **T2.2** fractional JDN + `datetime` not implemented | `ARCHITECTURE.md` canonical time model |
| `KurdishDate` has no `from_jdn` / `to_jdn` public API | Architecture doc |
| `Rojjmer` dual meaning of `(y,m,d)` (Gregorian vs Persian) is **documented** but **error-prone** | Prefer explicit factories `from_gregorian` / `from_persian` only (migration) |
| No **CHANGELOG.md** or migration guide | **T8.3** |
| Task file stale | Task Master hygiene |
| **Ruff** ruleset is minimal (`E`, `F`, `I`, `UP`); no `S` (bandit) or `B` (flake8-bugbear) in CI | Hardening |

---

## 4. Remediation Plan (prioritized)

### Phase A — Must-fix before “done” (security + API contract)

1. **Validate all public numeric inputs** on `KurdishDate` constructors and module-level helpers (`gregorian_to_*`, `*_to_gregorian`, and low-level `convert` functions intended for public use). Enforce:
   - `isinstance(..., int)` and **not** `bool` (or explicitly reject `bool`).
   - Month/day ranges per calendar; **year** within documented bounds (define constants, e.g. `MIN_YEAR`, `MAX_YEAR` or match `datetime`).
   - Raise **`PyrojRangeError`** / **`PyrojValueError`** per `ARCHITECTURE.md`; **never** plain `ValueError` for range issues in public API.
2. **Unify exceptions**: change `persian_days_in_month` (and any other internal `ValueError`) to **`PyrojRangeError`** where appropriate, or document that `convert` is internal-only and not covered by `Pyroj*`.
3. **Document** supported ranges and behavior for out-of-range input in **`SECURITY.md`** and `README.rst`/`README.md`.
4. **Sync TaskMaster JSON** or add `meta` field “last reviewed” + checklist so pending/done matches reality.

### Phase B — Strongly recommended (engineering maturity)

5. **CI (T9.1)**: Add GitHub Actions (or GitLab) workflow: run `pytest`, `ruff check`, `mypy` on Python 3.10–3.13.
6. **Pre-commit (T9.2)**: `.pre-commit-config.yaml` with ruff + end-of-file fixer.
7. **CHANGELOG + migration (T8.3)**: `CHANGELOG.md`, short “Migrating from 0.0.x” section (`Rojjmer`, `persiantools` removal).
8. **Logging (T7.2)**: Optional `debug` logging behind `os.environ.get("PYROJ_DEBUG")`, **no** PII or paths; document in `SECURITY.md`.

### Phase C — Feature completeness (optional for “v1.0” label)

9. **T6** locales + **T6.4** safe formatter (fixed token map only; no `eval`).
10. **T2.2** `datetime` / fractional JDN API if needed for parity with `KurdishDate` TS.
11. **T5.3** Nineveh era as separate enum + conversion module (isolated from default solar path).
12. **T10**: Deprecate `Rojjmer` at class level; set removal **version** in `DeprecationWarning` and CHANGELOG.

### Phase D — Hardening

13. Add **bandit** or **ruff** security-related rules in CI where applicable.
14. **Property tests** (optional dev dependency `hypothesis`) for round-trip invariants.

---

## 5. Definition of “fully done” (for this program)

Minimum bar before closing the Task Master epic:

- [ ] Phase **A** items complete and tests added for invalid inputs.
- [ ] Phase **B** items **5–7** complete (CI + CHANGELOG + exception consistency).
- [ ] `REFACTOR_TASKMASTER.json` updated or superseded by an accurate task export.
- [ ] `SECURITY.md` updated to reflect validation and logging behavior.

Optional (product-dependent):

- [ ] Phase **C** for **locales** and **Nineveh-era** if in scope for v1.
- [ ] Phase **D** for stricter static/security analysis.

---

## 6. References

- `docs/ARCHITECTURE.md` — intended design and threat model notes.
- `SECURITY.md` — reporting and secrets policy.
- `docs/REFACTOR_TASKMASTER.json` — task breakdown (update after remediation).
- OWASP guidance on **input validation** and **safe logging** (general principles; this library has no network surface).
