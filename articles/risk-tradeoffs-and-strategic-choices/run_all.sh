#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Running standard-library Python diagnostics..."
python3 python/risk_tradeoff_diagnostics.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R strategic tradeoff profile review..."
  Rscript r/strategic_tradeoff_profile_review.R
else
  echo "Rscript not found. Skipping R workflow."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia strategic tradeoff sensitivity model..."
  julia julia/strategic_tradeoff_sensitivity.jl
else
  echo "Julia not found. Skipping Julia workflow."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Creating SQLite schema..."
  sqlite3 outputs/tables/risk_tradeoffs_strategic_choices.sqlite < sql/schema.sql
else
  echo "sqlite3 not found. Skipping SQLite schema creation."
fi

echo "Done. Review outputs/tables and outputs/reports."
