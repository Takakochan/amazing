RM := rm -rf

MYPY_FLAGS += --warn-return-any
MYPY_FLAGS += --warn-unused-ignores
MYPY_FLAGS += --ignore-missing-imports
MYPY_FLAGS += --disallow-untyped-defs
MYPY_FLAGS += --check-untyped-defs

all: install run

install:
	uv tool install flake8
	uv tool install mypy
	uv tool install ruff
	uv tool install ty
	uv add numpy

run:
	uv run src/main.py

debug:
	# TODO: use pdb
	uv run src/main.py

clean:
	uvx ruff clean
	$(RM) .mypy_cache/
	$(RM) .ruff_cache/
	$(RM) .venv/

lint:
	uvx flake8 ./src/
	uvx mypy ./src/ $(MYPY_FLAGS)

lint-strict:
	uvx flake8 ./src/
	uvx mypy ./src/ --strict
	uvx ruff check
	uvx ty check

.PHONY: all install run debug clean lint lint-strict
