# Heuristics in Strategic Ideation

This article folder contains an advanced, strategist-facing companion scaffold for **"Heuristics in Strategic Ideation."**

The repository treats heuristics as strategic search-compression mechanisms: availability, representativeness, anchoring, recognition, satisficing, affect, default logic, social proof, expertise, institutional shortcuts, and complexity-mismatch risks shape which ideas appear before formal evaluation begins.

## Why this exists

Organizations cannot generate every possible strategic idea. They rely on shortcuts. The professional task is not to eliminate heuristics, but to diagnose which shortcuts are governing the search, whether they are useful for the context, where they narrow possibility, and how to build a richer heuristic ecology for strategy work.

This scaffold helps strategists review heuristic profiles, detect premature closure, score search breadth, audit institutional shortcuts, test complexity fit, design better stopping rules, and preserve decision memory around rejected, deferred, and unexplored options.

## Advanced strategist-facing capabilities

- Heuristic-profile diagnostics
- Search-breadth and heuristic-diversity scoring
- Availability, anchoring, recognition, satisficing, affect, default, and social-proof review
- Premature-closure and recognition-trap risk flags
- Expertise compression and expert-enclosure review
- Institutional shortcut and path-dependence audit
- Source-domain diversity and distant-analogy review
- Complexity-fit checks for heuristic validity
- Stopping-rule governance and search-closure review
- Decision-memory templates for rejected, deferred, and revisited ideas
- SQL schemas for sessions, heuristics, ideas, frames, assumptions, stakeholders, source domains, evaluations, and decision memory
- Optional advanced analytics with pandas and matplotlib
- Multi-language examples for reproducible heuristic analysis

## Folder structure

```text
python/      dependency-light diagnostics plus optional advanced analytics
r/           heuristic profile comparison, risk flags, and visualization
julia/       heuristic-search and scenario-sensitivity examples
sql/         schemas and analytical queries for heuristic-aware ideation systems
rust/        command-line heuristic diagnostics scaffold
go/          search-breadth review utility scaffold
cpp/         efficient scoring and profile examples
fortran/     weighted heuristic-profile scoring examples
c/           low-level heuristic-score utilities
docs/        strategist guides, templates, workshop tools, modeling principles
data/        synthetic heuristic and strategic ideation datasets
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
python3 python/heuristics_diagnostics.py
```

Optional advanced analytics:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r python/requirements-advanced.txt
python3 python/advanced_heuristics_analytics.py
```

## Main outputs

```text
outputs/tables/heuristic_context_profiles.csv
outputs/tables/premature_closure_risk.csv
outputs/tables/search_breadth_scores.csv
outputs/tables/heuristic_use_review.csv
outputs/tables/institutional_shortcut_audit.csv
outputs/tables/complexity_fit_review.csv
outputs/tables/stopping_rule_review.csv
outputs/tables/intervention_recommendations.csv
outputs/reports/heuristics_diagnostic_report.md
```

## Responsible use

These workflows use synthetic data and are designed for professional learning, strategic analysis, methods demonstration, institutional learning, and reproducible workflow development. They are not a substitute for stakeholder engagement, ethical review, domain expertise, accountable governance, or participatory judgment.
