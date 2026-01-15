.PHONY: clean build skills update-version docs test smoke coverage
.PHONY: coverage-smoke

LLMS_INCLUDE   = pyproject.toml,LICENSE,README.md,mindm/*,mindmap/*,examples/*,skills/*
LLMS_EXCLUDE   = mindm/as/*.md,llms.txt,update_version.py,examples/docs,examples/Test_DOM.*,mindm/__pycache__,mindmap/__pycache__,mindm/.DS_Store,mindm/as/*.scpt,mindm/as/MindManager.sdef.md,mindm/skills

# Default target
all: clean update-version build install skills test llms docs

# Clean the dist folder
clean:
	rm -rf dist/*
	rm -f mindm/skills/*.skill
	find . -name ".DS_Store" -print -delete

# Update version in pyproject.toml (increment last digit)
update-version:
	@python update_version.py

# Build the package
build: skills
	python -m build

# Package skills into .skill files
skills:
	python package_skills.py

# Install the package
install:
	pip install -e ".[dev]"

# llms
llms:
	pip install gitingest
	gitingest . -o llms.txt -i "$(LLMS_INCLUDE)" -e "$(LLMS_EXCLUDE)"

# Generate documentation
docs:
	cd docs && make clean html
	cd ..

# Run tests
test:
	python -m pytest

# Run MindManager smoke tests (requires running instance)
smoke:
	MINDM_SMOKE=1 python -m pytest -q

# Measure test coverage
coverage:
	python -m pytest -q --disable-warnings --cov=mindmap --cov=mindm --cov-report=term-missing:skip-covered

# Measure coverage including MindManager smoke tests
coverage-smoke:
	MINDM_SMOKE=1 python -m pytest -q --disable-warnings --cov=mindmap --cov=mindm --cov-report=term-missing:skip-covered

# Create a release on Github
release:
	@if [ -z "$$VERSION" ]; then \
		echo "Error: VERSION is required. Use 'make release VERSION=x.x.x'"; \
		exit 1; \
	fi
	@echo "Creating release v$$VERSION..."
	git tag -a v$$VERSION -m "Release v$$VERSION"
	git push origin v$$VERSION
	@echo "\nRelease v$$VERSION created."

# Help
help:
	@echo "Available targets:"
	@echo "  all            - Run clean, update-version, build, and docs"
	@echo "  clean          - Remove contents of dist folder"
	@echo "  update-version - Increment build number in pyproject.toml"
	@echo "  build          - Build the package with python -m build"
	@echo "  skills         - Package skills into .skill files in mindm/skills/"
	@echo "  install        - Install the package in editable mode"
	@echo "  llms           - Generate llms documentation"
	@echo "  docs           - Generate HTML documentation with clean option"
	@echo "  test           - Run test suite with pytest"
	@echo "  smoke          - Run MindManager smoke tests (requires MINDM_SMOKE=1)"
	@echo "  coverage       - Run tests with coverage report"
	@echo "  coverage-smoke - Run coverage including MindManager smoke tests"
	@echo "  release        - Create a release on GitHub"
	@echo "  help           - Show this help message"
