# Theory of Change and Strategic Logic

This article folder contains an advanced, strategist-facing companion scaffold for **"Theory of Change and Strategic Logic."**

The repository treats theory of change as a professional strategic discipline for connecting ideas to mechanisms, actors, assumptions, evidence, outcomes, feedback, implementation, and adaptive learning. It helps teams test whether a strategic idea has a plausible pathway from action to result before the idea becomes an expensive institutional commitment.

## Why this exists

Strategic ideas are often persuasive before they are valid. A strategy may sound coherent, fit the language of leadership, and appear aligned with institutional priorities while depending on weak causal links, untested assumptions, unrealistic actor responses, missing capacity, poor evidence, or hidden system effects. This scaffold helps strategists examine the pathway itself: what must happen, why it should happen, who must respond, what evidence supports each link, and what learning should change the strategy.

## Advanced strategist-facing capabilities

- Strategic logic and mechanism clarity diagnostics
- Theory-of-change causal link scoring
- Assumption criticality and uncertainty review
- Evidence strength, relevance, and transferability assessment
- Actor-response and stakeholder-dependency analysis
- Capacity and implementation readiness review
- System feedback, delay, adaptation, and burden-shift diagnostics
- Outcome sequencing and strategic time analysis
- Prototype-test design tied to causal links
- Implementation learning and revision-trigger design
- Option confidence scoring by theory-of-change quality
- Decision-memory records for theory revision
- SQL schemas for ideas, mechanisms, actors, assumptions, evidence, activities, outputs, outcomes, impact, prototypes, implementation reviews, revision triggers, and decisions
- Optional advanced analytics with pandas, numpy, and matplotlib
- Multi-language examples for reproducible strategic logic analysis

## Folder structure

```text
python/      dependency-light diagnostics plus optional advanced analytics
r/           theory-of-change link risk comparison and visualization
julia/       causal link sensitivity and theory confidence examples
sql/         schemas and analytical queries for theory-of-change analysis
rust/        command-line strategic logic diagnostics scaffold
go/          theory-of-change evaluation utility scaffold
cpp/         efficient link-risk scoring examples
fortran/     weighted causal-link scoring examples
c/           low-level strategic-logic score utilities
docs/        strategist guides, templates, workshop tools, modeling principles
data/        synthetic theory-of-change datasets
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
python3 python/theory_of_change_diagnostics.py
```

Optional advanced analytics:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r python/requirements-advanced.txt
python3 python/advanced_theory_of_change_analytics.py
```

## Main outputs

```text
outputs/tables/strategic_logic_scores.csv
outputs/tables/theory_link_risk_scores.csv
outputs/tables/assumption_link_review.csv
outputs/tables/evidence_match_review.csv
outputs/tables/actor_response_review.csv
outputs/tables/system_feedback_review.csv
outputs/tables/outcome_sequence_review.csv
outputs/tables/prototype_test_design_scores.csv
outputs/tables/implementation_learning_review.csv
outputs/tables/revision_trigger_review.csv
outputs/reports/theory_of_change_diagnostic_report.md
```

## Responsible use

These workflows use synthetic data and are designed for professional learning, strategic analysis, methods demonstration, institutional learning, and reproducible workflow development. They are not a substitute for stakeholder engagement, ethical review, domain expertise, accountable governance, or participatory judgment.
