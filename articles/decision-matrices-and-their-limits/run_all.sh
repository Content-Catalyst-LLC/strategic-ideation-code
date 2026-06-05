#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Running standard-library Python diagnostics..."
python3 python/decision_matrix_diagnostics.py
if command -v Rscript >/dev/null 2>&1; then Rscript r/matrix_sensitivity_review.R; else echo "Rscript not found. Skipping R workflow."; fi
if command -v julia >/dev/null 2>&1; then julia julia/matrix_sensitivity.jl; else echo "Julia not found. Skipping Julia workflow."; fi
if command -v sqlite3 >/dev/null 2>&1; then sqlite3 outputs/tables/decision_matrices_and_limits.sqlite < sql/schema.sql; else echo "sqlite3 not found. Skipping SQLite schema creation."; fi
echo "Done. Review outputs/tables and outputs/reports."
