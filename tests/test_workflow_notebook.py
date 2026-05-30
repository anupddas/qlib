"""
Lightweight structural tests for examples/workflow_by_code.ipynb.
These run fast (no data/model required) and catch notebook JSON issues
before the more expensive nbmake execution step runs.
"""
import json
import pathlib
import pytest

NOTEBOOK_PATH = pathlib.Path("examples") / "workflow_by_code.ipynb"


def test_notebook_exists():
    assert NOTEBOOK_PATH.exists(), f"Notebook not found: {NOTEBOOK_PATH}"


def test_notebook_is_valid_json():
    with open(NOTEBOOK_PATH, encoding="utf-8") as fh:
        nb = json.load(fh)
    assert nb.get("nbformat", 0) >= 4, "Notebook must be nbformat 4+"
    assert "cells" in nb, "Notebook JSON missing 'cells'"


def test_notebook_has_code_cells():
    with open(NOTEBOOK_PATH, encoding="utf-8") as fh:
        nb = json.load(fh)
    code_cells = [c for c in nb["cells"] if c.get("cell_type") == "code"]
    assert len(code_cells) > 0, "No code cells found in notebook"


def test_notebook_outputs_are_stripped():
    """Outputs should be stripped before committing (use nbstripout)."""
    with open(NOTEBOOK_PATH, encoding="utf-8") as fh:
        nb = json.load(fh)
    for cell in nb["cells"]:
        if cell.get("cell_type") == "code":
            assert cell.get("outputs", []) == [], (
                f"Stale outputs in cell: {str(cell.get('source',''))[:60]}…\n"
                "Run: nbstripout examples/workflow_by_code.ipynb"
            )
