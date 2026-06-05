#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Running standard-library Python diagnostics..."
python3 python/option_value_diagnostics.py
if command -v Rscript >/dev/null 2>&1; then
  echo "Running R strategic option value profile review..."
  Rscript r/strategic_option_value_review.R
else
  echo "Rscript not found. Skipping R workflow."
fi
if command -v julia >/dev/null 2>&1; then
  echo "Running Julia option value sensitivity model..."
  julia julia/option_value_sensitivity.jl
else
  echo "Julia not found. Skipping Julia workflow."
fi
if command -v sqlite3 >/dev/null 2>&1; then
  echo "Creating SQLite schema..."
  sqlite3 outputs/tables/option_value_strategic_flexibility.sqlite < sql/schema.sql
else
  echo "sqlite3 not found. Skipping SQLite schema creation."
fi
echo "Done. Review outputs/tables and outputs/reports."
