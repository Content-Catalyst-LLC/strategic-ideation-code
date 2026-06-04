# Strategy vs Tactics vs Ideation

This article folder contains an advanced, strategist-facing companion scaffold for **"Strategy vs Tactics vs Ideation."**

The repository treats ideation, strategy, tactics, and learning as separate but connected layers of strategic decision-making. It is designed for professional strategy work: layered diagnosis, alignment review, portfolio governance, tactical translation, assumption testing, feedback routing, decision memory, and adaptive learning.

## Why this exists

Strategy teams often misdiagnose failure. A tactical problem may really be a strategy problem. A strategy problem may originate in weak ideation. A learning problem may occur because feedback is collected but never routed to the layer that can use it. This scaffold provides practical tools for identifying the real failure point.

## Advanced strategist-facing capabilities

- Layered diagnosis of conceptual, directional, operational, and learning failures
- Strategy-to-tactics alignment scoring
- Strategic initiative portfolio scoring
- Tactical translation and execution-coherence review
- Assumption criticality and confidence analysis
- Feedback routing by decision layer
- Decision-memory and rejected-alternative documentation
- Layer-specific meeting and workshop templates
- SQL schemas for strategy systems and institutional memory
- Optional advanced analytics with pandas and matplotlib
- Multi-language examples for reproducible strategic analysis

## Folder structure

```text
python/      standard-library diagnostics plus optional advanced analytics
r/           portfolio comparison, tradeoff visualization, revision flags
julia/       scenario-comparison and layer-alignment examples
sql/         schemas and analytical queries for strategy systems
rust/        command-line layer-diagnostics scaffold
go/          strategy-to-tactics alignment utility scaffold
cpp/         efficient scoring and portfolio examples
fortran/     weighted alignment scoring examples
c/           low-level alignment-score utilities
docs/        strategist guides, templates, workshop tools, modeling principles
data/        synthetic strategy datasets
outputs/     generated tables, figures, and reports
notebooks/   notebook placeholders
```

## Quick start

From this article folder:

```bash
./run_all.sh
```

Or run the main diagnostic directly:

```bash
python3 python/layer_alignment_diagnostics.py
```

Optional advanced analytics:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r python/requirements-advanced.txt
python3 python/advanced_layer_analytics.py
```

## Main outputs

```text
outputs/tables/layer_alignment_scores.csv
outputs/tables/initiative_portfolio_scores.csv
outputs/tables/tactical_translation_gaps.csv
outputs/tables/feedback_routing_recommendations.csv
outputs/reports/strategist_diagnostic_report.md
```

## Responsible use

These workflows use synthetic data and are designed for professional learning, strategy analysis, methods demonstration, and reproducible workflow development. They are not a substitute for stakeholder engagement, domain expertise, ethical review, accountable governance, or participatory judgment.
