# Contributing Guidelines

Thank you for contributing to **pyroj**! To maintain the highest quality and reliability of the project, please adhere to the following rules when proposing any changes to the codebase.

## ⚠️ Core Rule: The Documentation-Sync Mandate

Whenever you update, modify, or add any logical features to the Python code (e.g., changes to behavior, internal data shapes, mappings, types, or API signatures), you **must concurrently update**:

1. **The Tests**: Validate any new alternative names, bounds, types, or formatting logic.
2. **The Documentation**: Keep the README.md usage patterns and snippets perfectly up-to-date with the new API.
3. **The Locale Reference Docs**: E.g. `docs/LOCALES.md` and `docs/kurdish_months.md` must be synchronized so users have a fully updated map of dialect aliases.

Any Pull Request that updates the codebase but fails to provide the accompanying documentation and test additions will not be merged.

## Running Tests

`pyroj` leverages `uv` and `pytest` for automated analysis. You must ensure you run all checks before submitting patches:

```bash
uv sync --extra dev
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run pytest
```

If `mypy` or `ruff` flags your changes, please fix them before submitting! Ensure test coverage accommodates your edge-cases cleanly.
