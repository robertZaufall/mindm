.PHONY: clean build update-version docs

LLMS_INCLUDE   = pyproject.toml,LICENSE,README.md,mindm/*,mindmap/*,examples/*
LLMS_EXCLUDE   = mindm/as/*.md,llms.txt,update_version.py,examples/docs,examples/Test_DOM.*,mindm/__pycache__,mindmap/__pycache__,mindm/.DS_Store,mindmap/.DS_Store,mindm/as/*.scpt

# Default target
all: clean update-version build install llms docs

# Clean the dist folder
clean:
	rm -rf dist/*

# Update version in pyproject.toml (increment last digit)
update-version:
	@python update_version.py

# Build the package
build:
	python -m build

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
	@echo "  install        - Install the package in editable mode"
	@echo "  llms           - Generate llms documentation"
	@echo "  docs           - Generate HTML documentation with clean option"
	@echo "  release        - Create a release on GitHub"
	@echo "  help           - Show this help message"