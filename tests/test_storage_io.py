"""Regression coverage for dags/utils/storage_io.py's local-mode functions.

These are plain functions with no Airflow or GCS dependency in "local" mode
(the default - see storage_paths.get_storage_mode), so they're testable
without installing Airflow, which isn't even in requirements.txt and is only
actually available inside the Airflow container/image.

Motivation: check_duplicates() in dags/data_quality_dag.py had
`for f in join_path(curated_zone):` where every sibling function in the same
file correctly uses `for f in list_files(curated_zone):` - a copy-paste typo
that raises TypeError (join_path takes two required args) every time that
quality check runs. Nothing caught it because there was no test coverage
touching this module at all. This file doesn't import data_quality_dag
directly (that still needs Airflow to import), but it locks down the two
functions whose misuse caused the bug, and reproduces the exact loop shape
those DAG tasks use.
"""
from __future__ import annotations

import os
import sys

# dags/utils/storage_io.py imports its sibling as `from utils.storage_paths
# import ...`, which only resolves with dags/ itself on sys.path - that's
# the layout Airflow's DAG folder scanning assumes, not a `dags.utils`
# package importable from the project root conftest.py already adds.
_DAGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dags"))
if _DAGS_DIR not in sys.path:
    sys.path.insert(0, _DAGS_DIR)

from utils.storage_io import join_path, list_files  # noqa: E402


def test_list_files_returns_filenames_not_a_path_string(tmp_path):
    (tmp_path / "a.csv").write_text("x")
    (tmp_path / "b.csv").write_text("y")

    files = list_files(str(tmp_path))

    assert sorted(files) == ["a.csv", "b.csv"]


def test_list_files_on_a_missing_directory_is_empty_not_an_error(tmp_path):
    assert list_files(str(tmp_path / "does-not-exist")) == []


def test_join_path_requires_both_a_base_and_a_filename():
    assert join_path("curated", "data.csv") == os.path.join("curated", "data.csv")


def test_the_list_files_then_join_path_loop_shape_used_by_the_dq_checks(tmp_path):
    """The exact pattern check_schema_conformance / check_null_ratios /
    check_row_counts / check_duplicates all use: list the directory, then
    join_path each name back onto it to get a readable path. Calling
    join_path(dir) alone - the bug this file exists to catch - raises
    TypeError before ever reaching a file.
    """
    (tmp_path / "curated.csv").write_text("a,b\n1,1\n1,1\n2,2\n")

    seen = []
    for name in list_files(str(tmp_path)):
        if not name.endswith(".csv"):
            continue
        path = join_path(str(tmp_path), name)
        assert os.path.isfile(path)
        seen.append(name)

    assert seen == ["curated.csv"]
