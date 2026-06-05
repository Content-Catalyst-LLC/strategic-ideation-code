#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Running standard-library Python diagnostics..."
python3 python/idea_to_strategy_diagnostics.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R idea-to-strategy profile review..."
  Rscript r/idea_to_strategy_profile_review.R
else
  echo "Rscript not found. Skipping R workflow."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia strategy conversion sensitivity model..."
  julia julia/strategy_conversion_sensitivity.jl
else
  echo "Julia not found. Skipping Julia workflow."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Creating SQLite schema..."
  sqlite3 outputs/tables/from_ideas_to_strategy.sqlite < sql/schema.sql
else
  echo "sqlite3 not found. Skipping SQLite schema creation."
fi

echo "Done. Review outputs/tables and outputs/reports."
