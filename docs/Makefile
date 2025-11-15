# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

GITINGEST     ?= gitingest
LLMS_OUTPUT    = $(BUILDDIR)/html/llms.txt
LLMS_INCLUDE   = pyproject.toml,LICENSE,README.md,mindm/*,mindmap/*,examples/*
LLMS_EXCLUDE   = llms.txt,update_version.py,examples/docs,examples/Test_DOM.*,mindm/__pycache__,mindmap/__pycache__,mindm/.DS_Store,mindmap/.DS.Store,mindm/as/*.scpt

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@$(MAKE) llms

.PHONY: help llms Makefile

llms:
	@mkdir -p $(dir $(LLMS_OUTPUT))
	@$(GITINGEST) ../. -o $(LLMS_OUTPUT) -i "$(LLMS_INCLUDE)" -e "$(LLMS_EXCLUDE)"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@$(MAKE) llms
