RM := rm -rf

FLAKE8_FLAGS += --color always
MYPY_FLAGS += --color-output
MYPY_FLAGS += --warn-return-any
MYPY_FLAGS += --warn-unused-ignores
MYPY_FLAGS += --ignore-missing-imports
MYPY_FLAGS += --disallow-untyped-defs
MYPY_FLAGS += --check-untyped-defs
RUFF_FORMAT_CHECK_FLAGS += --color always
RUFF_CHECK_FLAGS += --color always
TY_CHECK_FLAGS += --color always

MAIN_PROGRAM := a_maze_ing.py

all: install run

install:
	uv tool install flake8
	uv tool install mypy
	uv tool install ruff
	uv tool install ty
	uv add numpy

run:
	uv run $(MAIN_PROGRAM) config.txt

debug:
	# TODO: use pdb
	uv run $(MAIN_PROGRAM)

clean:
	uvx ruff clean
	$(RM) .mypy_cache/
	$(RM) .ruff_cache/
	$(RM) .venv/

lint:
	uvx flake8 $(FLAKE8_FLAGS) .
	uvx mypy $(MYPY_FLAGS) .

lint-strict:
	uvx flake8 $(FLAKE8_FLAGS) .
	uvx mypy $(MYPY_FLAGS) --strict .
	uvx ruff format --check $(RUFF_FORMAT_CHECK_FLAGS)
	uvx ruff check $(RUFF_CHECK_FLAGS)
	uvx ty check $(TY_CHECK_FLAGS)

format:
	uvx ruff check --fix --select=I001
	uvx ruff format

.PHONY: all install run debug clean lint lint-strict format
