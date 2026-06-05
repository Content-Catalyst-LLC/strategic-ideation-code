# Assumption Mapping for Strategic Ideas

This article folder contains an advanced, strategist-facing companion scaffold for **"Assumption Mapping for Strategic Ideas."**

The repository treats assumption mapping as a professional strategic discipline for identifying, testing, prioritizing, and revising the beliefs that must be true for a strategic idea to work. It supports criticality and uncertainty scoring, evidence review, prototype learning design, theory-of-change assumption mapping, option confidence scoring, stakeholder sensitivity review, implementation capacity checks, system response diagnostics, future-facing assumption review, revision triggers, and decision memory.

## Why this exists

Strategic ideas often fail because teams confuse coherent logic with validated logic. An idea may be persuasive, aligned, and feasible on paper while depending on untested assumptions about behavior, trust, capacity, incentives, technology, evidence transfer, system response, legitimacy, and future conditions. This scaffold helps strategists make those assumptions visible before they become expensive commitments.

## Advanced strategist-facing capabilities

- Assumption criticality and uncertainty scoring
- Evidence-adjusted assumption risk
- Test prioritization and learning-value scoring
- Behavioral, stakeholder, capacity, technology, market, institutional, system, ethical, and future-facing assumption review
- Evidence strength, relevance, and transferability assessment
- Prototype test design linked to critical assumptions
- Theory-of-change assumption review
- Option confidence and commitment-risk scoring
- Assumption aging and decay monitoring
- Revision-trigger design
- Decision-memory records
- SQL schemas for ideas, assumptions, evidence, tests, stakeholders, theory-of-change links, options, prototypes, revision triggers, reviews, and decisions
- Optional advanced analytics with pandas, numpy, and matplotlib
- Multi-language examples for reproducible assumption mapping

## Folder structure

```text
python/      dependency-light diagnostics plus optional advanced analytics
r/           assumption risk comparison and visualization
julia/       assumption sensitivity and option confidence examples
sql/         schemas and analytical queries for assumption mapping
rust/        command-line assumption diagnostics scaffold
go/          assumption-prioritization utility scaffold
cpp/         efficient assumption scoring examples
fortran/     weighted assumption scoring examples
c/           low-level assumption score utilities
docs/        strategist guides, templates, workshop tools, modeling principles
data/        synthetic assumption mapping datasets
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
python3 python/assumption_mapping_diagnostics.py
```

Optional advanced analytics:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r python/requirements-advanced.txt
python3 python/advanced_assumption_analytics.py
```

## Main outputs

```text
outputs/tables/assumption_risk_scores.csv
outputs/tables/evidence_review_scores.csv
outputs/tables/test_prioritization_scores.csv
outputs/tables/prototype_learning_scores.csv
outputs/tables/theory_of_change_assumption_scores.csv
outputs/tables/option_confidence_scores.csv
outputs/tables/stakeholder_assumption_review.csv
outputs/tables/system_response_assumption_review.csv
outputs/tables/future_assumption_review.csv
outputs/tables/revision_trigger_review.csv
outputs/reports/assumption_mapping_diagnostic_report.md
```

## Responsible use

These workflows use synthetic data and are designed for professional learning, strategic analysis, methods demonstration, institutional learning, and reproducible workflow development. They are not a substitute for stakeholder engagement, ethical review, domain expertise, accountable governance, or participatory judgment.
