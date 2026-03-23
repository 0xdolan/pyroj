# Security

## Reporting

Report sensitive vulnerabilities through the repository’s private security advisory channel or maintainer contact on the GitHub project page—not in public issues.

## Development practices

- **No secrets in git**: API keys, tokens, passwords, and personal MCP `mcp.json` files must not be committed. Use `.cursor/mcp.json.example` as a template; keep real configs local and gitignored.
- **Dependencies**: v2 targets **stdlib-only** runtime to minimize supply-chain surface. Development dependencies are managed from `pyproject.toml` using `uv` (avoid `requirements.txt` drift).
- **Input validation**: All calendar components validate year/month/day ranges before conversion. Do not use `eval`, `exec`, or `pickle` on untrusted input in library code.
- **Logging**: Do not log environment variables, auth headers, or full user paths by default.

## Threat model (library)

Pyroj is a date conversion library; it does not execute network calls or subprocesses. Primary risks are incorrect date arithmetic (mitigated by tests) and unsafe string formatting if user-controlled format strings are ever added—prefer fixed token maps for formatting APIs.

The `format_calendar_date` API only interprets a **fixed token vocabulary**; patterns must not contain `{`, `}`, or `%`. There is no `eval`, `exec`, or dynamic `str.format` on user input. Maximum pattern length is capped to reduce abuse.
