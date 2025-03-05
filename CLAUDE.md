# CLAUDE.md - Guidelines for mindm project

## Build & Development Commands
- Build package: `python -m build`
- Install development dependencies: `pip install -e ".[dev,docs]"`
- Format code: `black .`
- Lint code: `flake8`
- Run all tests: `pytest`
- Run single test: `pytest tests/test_file.py::TestClass::test_method`
- Build docs: `cd docs && make html`

## Code Style Guidelines
- **Formatting**: Use Black formatter
- **Imports**: Standard library first, then third-party, then local modules
- **Typing**: Type annotations encouraged but not required
- **Naming**:
  - Classes: PascalCase (MindmapDocument, MindmapTopic)
  - Methods/Functions: snake_case (get_mindmap, create_mindmap)
  - Variables: snake_case (guid_mapping, central_topic)
- **Error Handling**: Use try/except with specific exceptions
- **Documentation**: Use double-quoted docstrings in RST format
- **Testing**: Use unittest with extensive mocking

## Project Structure
- **mindm/**: Core module for MindManager interaction
- **mindmap/**: Module for mindmap data structures and operations
- **examples/**: Example usage scripts