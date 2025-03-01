# CLAUDE.md - Guide for Mindm Project

## Development Commands
```bash
# Build package
python -m build

# Installation (development mode)
pip install -e .

# Run tests
python -m unittest discover tests  # Run all tests
python -m unittest tests/test_mindmap_helper.py  # Run specific test file
python -m unittest tests.test_mindmap_helper.TestMindmapClasses.test_mindmap_link_init  # Run specific test case

# Generate documentation
cd docs
make html       # Generate HTML docs
make clean html # Rebuild docs from scratch
# View docs in browser
open _build/html/index.html

# Sphinx settings in conf.py
# - Set html_show_sourcelink = False to hide "Show Source" links
# - Set html_copy_source = False to prevent source copying
# - Use custom CSS to hide unwanted sidebar elements
```

## Documentation
The project uses Sphinx with autodoc to generate documentation:
- `conf.py` - Configuration file for Sphinx
- RST files define the documentation structure
- Documentation is built from docstrings in the code
- Napoleon extension allows Google-style docstrings
- Viewcode extension shows source code in the docs

To show documentation for platform-specific modules:
- Create custom RST files for platform-specific modules using regex parsing
- Extract method signatures and docstrings directly from source files
- Use the include directive to incorporate these into the main documentation
- Combine with literalinclude for complete source code display

## Code Style Guidelines
- **Imports**: Standard library first, third-party second, local imports last
- **Naming**: Classes in CamelCase, functions/variables in snake_case, constants in UPPER_SNAKE_CASE
- **Type annotations**: Use return type annotations and parameter type hints
- **Error handling**: Use try/except blocks with specific exceptions, print error messages with function context
- **Formatting**: 4-space indentation, blank lines between methods, reasonable function length
- **Docstrings**: Google-style format with Args: and Returns: sections:
  ```python
  def function_name(param1, param2):
      """Short description of function.
      
      Longer description if needed.
      
      Args:
          param1 (type): Description of param1.
          param2 (type): Description of param2.
      
      Returns:
          return_type: Description of return value.
      """
  ```

## Platform Support
Code handles platform-specific implementations via separate modules:
- `mindmanager_win.py` for Windows
- `mindmanager_mac.py` for macOS

Handle platform detection appropriately when making changes.

## Testing Guidelines
The project has a comprehensive testing suite that covers the mindmap helper functionality:

- **Test Files**:
  - `test_mindmap_helper.py` - Tests for basic class functionality and methods
  - `test_mindmap_relationships.py` - Tests for relationships between topics
  - `test_mindmap_creation.py` - Tests for creating and updating mindmaps

- **Testing Patterns**:
  - Use mocking to avoid relying on actual MindManager application
  - Test both normal cases and edge cases (empty values, circular references)
  - Ensure all tests are independent (don't rely on state from other tests)
  - When adding new functionality, add corresponding tests

- **Running Tests**:
  - Always run all tests before committing changes
  - If tests fail, fix the test or the implementation code as appropriate
  - Ensure tests run in reasonable time (< 1 second)