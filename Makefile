.PHONY: clean build update-version docs

# Default target
all: clean update-version build install docs

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
	pip install -e .

# Generate documentation
docs:
	cd docs && make clean html

# Help
help:
	@echo "Available targets:"
	@echo "  all            - Run clean, update-version, build, and docs"
	@echo "  clean          - Remove contents of dist folder"
	@echo "  update-version - Increment build number in pyproject.toml"
	@echo "  build          - Build the package with python -m build"
	@echo "  docs           - Generate HTML documentation with clean option"
	@echo "  help           - Show this help message"