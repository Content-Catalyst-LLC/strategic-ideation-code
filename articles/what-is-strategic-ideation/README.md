# What Is Strategic Ideation?

This article folder contains companion code and synthetic data for the article **"What Is Strategic Ideation?"**

The examples model strategic ideation as a structured process of:

- idea portfolio scoring
- strategic fit assessment
- option architecture
- assumption mapping
- tradeoff visualization
- scenario comparison
- prototype and implementation tracking
- revision flags and learning loops

These examples are designed for synthetic-data research, methods demonstration, institutional learning, and reproducible strategic analysis. They are not a substitute for participatory judgment, ethical review, stakeholder engagement, or domain expertise.

## Folder structure

```text
python/      idea portfolio scoring, strategic fit, option architecture, assumption mapping
r/           portfolio comparison, tradeoff visualization, revision flags
julia/       strategic scoring and scenario-comparison examples
sql/         ideas, criteria, assumptions, evaluation, prototypes, implementation schemas
rust/        command-line idea diagnostics scaffold
go/          option-evaluation utility scaffold
cpp/         efficient scoring and portfolio examples
fortran/     weighted scoring examples
c/           low-level idea-score utilities
docs/        article notes and modeling principles
data/        synthetic datasets
outputs/     generated outputs
notebooks/   notebook placeholders
```

## Suggested workflows

From this article folder:

```bash
python3 python/idea_portfolio_scoring.py
Rscript r/portfolio_comparison.R
julia julia/scenario_comparison.jl
sqlite3 strategic_ideation.sqlite < sql/schema.sql
```

Language-specific examples are intentionally simple enough to inspect and adapt.
