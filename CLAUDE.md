# Build and Test Commands
- Build package: `make build`
- Install package: `make install`
- Generate docs: `make docs`
- Run all tests: `pytest`
- Run single test: `pytest tests/test_file.py::test_function -v`
- Lint code: `flake8 mindm/ mindmap/`
- Format code: `black mindm/ mindmap/`

# Code Style Guidelines
- Follow PEP 8 standards
- Use 4-space indentation
- Add type annotations for all parameters and return values
- Use descriptive variable/function names (snake_case)
- Document classes and methods with docstrings
- Standard import order: standard lib → third-party → local modules
- Include comprehensive error handling with try/except blocks
- Package versioning managed via `update_version.py`
- Use comments sparingly - prefer self-documenting code