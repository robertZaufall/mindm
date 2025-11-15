# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	mkdir -p _build/html
	gitingest ../. -o _build/html/llms.txt -i "pyproject.toml,LICENSE,README.md,mindm/*,mindmap/*,examples/*" -e "llms.txt,update_version.py,examples/docs,examples/Test_DOM.*,mindm/__pycache__,mindmap/__pycache__,mindm/.DS_Store,mindmap/.DS.Store,mindm/as/*.scpt"

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	mkdir -p _build/html
	gitingest ../. -o _build/html/llms.txt -i "pyproject.toml,LICENSE,README.md,mindm/*,mindmap/*,examples/*" -e "llms.txt,update_version.py,examples/docs,examples/Test_DOM.*,mindm/__pycache__,mindmap/__pycache__,mindm/.DS_Store,mindmap/.DS.Store,mindm/as/*.scpt"
