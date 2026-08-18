CONFIG  ?= config.txt
PYTHON  = python3
MAIN    = a_maze_ing.py


install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e ".[dev]"

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name "*.egg-info" -o -name "dist" -o -name "build" \) -exec rm -rf {} + 2>/dev/null || true
	find . -type f \( -name "*.pyc" -o -name "*.whl" -o -name "*.tar.gz" \) -delete 2>/dev/null || true

lint:
	flake8 . --exclude=.venv
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude .venv

lint-strict:
	flake8 . --exclude=.venv
	mypy . --strict --exclude .venv

build:
	$(PYTHON) -m pip install --quiet build setuptools wheel
	$(PYTHON) -m build --no-isolation --outdir .

.PHONY: install run debug clean lint lint-strict build
