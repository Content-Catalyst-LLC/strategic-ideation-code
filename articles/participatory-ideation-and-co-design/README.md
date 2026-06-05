# Participatory Ideation and Co-Design

This article folder contains an advanced, strategist-facing companion scaffold for **"Participatory Ideation and Co-Design."**

The repository treats participation as a strategic capability: who is represented, who has influence, whose knowledge counts, how power is handled, how access is designed, how conflict is documented, how input changes decisions, and how organizations remain accountable after participation ends.

## Why this exists

Strategic ideas often fail because they are framed and developed by institutional insiders before affected users, workers, communities, or stakeholders have meaningful influence. This scaffold helps teams evaluate whether participation is substantive, accessible, reciprocal, power-aware, decision-linked, and accountable rather than tokenistic, extractive, or performative.

## Advanced strategist-facing capabilities

- Stakeholder and affected-group mapping
- Participation-quality diagnostics
- Representation coverage analysis
- Influence-boundary review
- Accessibility and participation-support review
- Reciprocity and participant-labor review
- Power-risk analysis
- Knowledge-integration scoring
- Conflict, disagreement, and tradeoff registers
- Co-design method fit assessment
- Decision-traceability records
- Accountability and close-the-loop review
- Tokenism and extraction risk scoring
- Participatory learning-memory records
- SQL schemas for stakeholders, sessions, influence boundaries, access supports, contributions, synthesis, conflict registers, decision traceability, accountability records, and learning memory
- Optional advanced analytics with pandas, numpy, and matplotlib
- Multi-language examples for reproducible co-design analysis

## Folder structure

```text
python/      dependency-light diagnostics plus optional advanced analytics
r/           participatory ideation profile comparison and visualization
julia/       participation, influence, and idea-quality sensitivity examples
sql/         schemas and analytical queries for participatory systems
rust/        command-line co-design diagnostics scaffold
go/          participation-quality evaluation utility scaffold
cpp/         efficient participation scoring examples
fortran/     weighted co-design profile examples
c/           low-level co-design score utilities
docs/        strategist guides, templates, workshop tools, modeling principles
data/        synthetic participatory ideation and co-design datasets
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
python3 python/participatory_codesign_diagnostics.py
```

Optional advanced analytics:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r python/requirements-advanced.txt
python3 python/advanced_participatory_analytics.py
```

## Main outputs

```text
outputs/tables/participation_system_profile_scores.csv
outputs/tables/stakeholder_representation_scores.csv
outputs/tables/influence_boundary_scores.csv
outputs/tables/accessibility_support_scores.csv
outputs/tables/reciprocity_scores.csv
outputs/tables/power_risk_scores.csv
outputs/tables/knowledge_integration_scores.csv
outputs/tables/conflict_tradeoff_scores.csv
outputs/tables/decision_traceability_scores.csv
outputs/tables/accountability_scores.csv
outputs/reports/participatory_codesign_diagnostic_report.md
```

## Responsible use

These workflows use synthetic data and are designed for professional learning, strategic analysis, methods demonstration, institutional learning, and reproducible workflow development. They are not a substitute for genuine participation, ethical review, community accountability, accessibility planning, facilitation judgment, domain expertise, or responsible governance.
