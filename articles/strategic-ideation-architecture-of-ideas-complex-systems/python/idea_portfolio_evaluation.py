"""
Strategic Ideation: Idea Portfolio Evaluation

Educational model for scoring ideas across multiple strategic dimensions.
"""

from __future__ import annotations

import pandas as pd


WEIGHTS = {
    "novelty": 0.16,
    "relevance": 0.20,
    "feasibility": 0.16,
    "strategic_fit": 0.20,
    "learning_potential": 0.14,
    "risk": -0.08,
    "implementation_readiness": 0.14
}


def weighted_idea_score(row: pd.Series) -> float:
    """Compute a weighted strategic idea score."""
    return sum(row[dimension] * weight for dimension, weight in WEIGHTS.items())


def main() -> None:
    ideas = pd.read_csv("../data/strategic_idea_portfolio.csv")
    ideas["idea_score"] = ideas.apply(weighted_idea_score, axis=1)

    ideas["needs_revision"] = (
        (ideas["feasibility"] < 0.60)
        | (ideas["risk"] > 0.45)
        | (ideas["implementation_readiness"] < 0.60)
    )

    ideas = ideas.sort_values("idea_score", ascending=False)

    print(ideas)

    ideas.to_csv("../outputs/idea_portfolio_scores.csv", index=False)


if __name__ == "__main__":
    main()
