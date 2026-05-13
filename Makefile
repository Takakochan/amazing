MAIN_PROGRAM := a_maze_ing.py

FLAKE8_FLAGS += --color always
FLAKE8_FLAGS += --exclude .mypy_cache,.pytest_cache,.ruff_cache,.venv
MYPY_FLAGS += --color-output
MYPY_FLAGS += --warn-return-any
MYPY_FLAGS += --warn-unused-ignores
MYPY_FLAGS += --ignore-missing-imports
MYPY_FLAGS += --disallow-untyped-defs
MYPY_FLAGS += --check-untyped-defs
RUFF_FORMAT_CHECK_FLAGS += --color always
RUFF_CHECK_FLAGS += --color always
TY_CHECK_FLAGS += --color always

RM := rm -rf

all: install run

install:
	@echo "This program has no dependencies."

run:
	uv run $(MAIN_PROGRAM) config.txt

debug:
	uv run python -m pdb $(MAIN_PROGRAM) config.txt

test:
	uvx pytest

clean:
	uvx ruff clean
	$(RM) .mypy_cache/
	$(RM) .pytest_cache/
	$(RM) .ruff_cache/
	$(RM) .venv/
	$(RM) mazegen.egg-info/

	find . -type d -name "__pycache__" -exec $(RM) {} +

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

build:
	uvx --from build pyproject-build --outdir ./

.PHONY: all install run debug test clean lint lint-strict format build
