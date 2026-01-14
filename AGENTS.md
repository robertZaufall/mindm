# Repository Guidelines

## Project Structure & Module Organization
`mindm/` hosts the platform connectors (`mindmanager.py`, `mindmanager_win.py`, `mindmanager_mac*.py`) with direct MindManager automation hooks, while `mindmap/` provides the higher-level document model plus serialization helpers (`serialization.py`, `export.py`, `import.py`). Codex skills live in `skills/` (see `skills/mindm-export`) and are packaged to `dist/`. Reference material lives in `docs/` (Sphinx) and publishes via `docs/_build/html`. Usage snippets and sanity scripts sit in `examples/`. Tweak version bumps through `update_version.py`, and manage builds with the root `Makefile`.

## Build, Test, and Development Commands
- `pip install -e ".[dev]"`: install editable package with dev tools needed for linting, docs, and tests.  
- `make build`: run `python -m build` to produce wheels/sdists into `dist/`.  
- `make docs`: clean and rebuild the Sphinx docs (`docs/_build/html`).  
- `MINDM_SMOKE=1 pytest -q`: quick smoke run against a connected MindManager instance.  
- `pytest` or `python -m pytest`: execute automated tests when you add them under `tests/` or `examples/`.
 - `make coverage` / `make coverage-smoke`: coverage reports (smoke includes live MindManager tests).

## Coding Style & Naming Conventions
Target Python 3.9+, 4-space indentation, and type hints on new public APIs. Keep modules and functions in `snake_case`, classes in `PascalCase`, and constants upper snake (`DUPLICATED_TAG`). Format with `black` (88 char line width) and lint via `flake8`; run both before pushing. Favor docstrings that match Sphinx’ Google-style sections so API docs stay coherent.

## Testing Guidelines
Use `pytest` for unit and integration coverage, naming files `test_*.py` and functions `test_*`. Mock MindManager COM or AppleScript boundaries so tests can run without the desktop app where possible; reserve `examples/test.py` for live end-to-end checks. Validate new serialization or import logic with round-trip tests and aim for coverage on new code paths before requesting review.

## Commit & Pull Request Guidelines
Follow the existing short, imperative commit style (`more examples added`, `extended AppleScript use`). Each PR should describe the scenario, platform impact (Windows/macOS), and any MindManager prerequisites. Link to GitHub issues when applicable, include CLI output or screenshots for doc changes, and tick off `make build`/`make docs`/`pytest` status so reviewers know everything passes.

## Documentation & Release Tips
Document API additions in `docs/*.rst`, then run `make docs` to confirm clean builds. When preparing a release, use `make release VERSION=x.y.z` after bumping via `make update-version`, and ensure `dist/` artifacts come from the matching commit.
