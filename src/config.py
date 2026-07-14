"""Shared paths and constants for the Student Success Intelligence Platform."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
EXPORT_DIR = DATA_DIR / "exports"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
REPORTS_DIR = PROJECT_ROOT / "reports" / "generated"

DUCKDB_PATH = WAREHOUSE_DIR / "student_success.duckdb"
RANDOM_SEED = 20260714
MODEL_VERSION = "student-risk-logistic-regression-v1.0.0"

for directory in [SYNTHETIC_DIR, EXPORT_DIR, WAREHOUSE_DIR, ARTIFACTS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
