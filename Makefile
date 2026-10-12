# Build the CV. `make` alone builds everything.
#
# Everything is generated from content/ + variants/ via scripts/build.py.
# There are no hand-edited artifacts anywhere in this repository.

PYTHON ?= python3
VENV   ?= .venv
BIN     = $(VENV)/bin

.DEFAULT_GOAL := all
.PHONY: all setup build one site clean check

all: build site

# One-time local setup.
setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt
	@echo
	@echo "Now run:  make build"

# Build every variant to PDF, DOCX and HTML. Fails if a PDF has no text layer.
build:
	PATH="$(BIN):$$PATH" $(BIN)/python scripts/build.py

# Build a single variant:  make one VARIANT=identity-security.en
one:
	PATH="$(BIN):$$PATH" $(BIN)/python scripts/build.py $(VARIANT)

# Generate the GitHub Pages landing page.
site:
	PATH="$(BIN):$$PATH" $(BIN)/python scripts/site.py

# Fast pre-commit sanity check: parses every YAML, reports placeholders,
# confirms the photo exists. Does not render.
check:
	@$(BIN)/python -c "import yaml" 2>/dev/null || $(MAKE) setup
	PATH="$(BIN):$$PATH" $(BIN)/python -c "import sys; sys.path.insert(0,'scripts')" \
	  && PATH="$(BIN):$$PATH" $(BIN)/python scripts/check.py

clean:
	rm -rf dist