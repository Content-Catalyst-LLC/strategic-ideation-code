#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 python/idea_portfolio_scoring.py
