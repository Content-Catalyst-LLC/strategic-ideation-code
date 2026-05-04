"""
Strategic Ideation: Assumption Mapping

Educational example for prioritizing assumptions by confidence and impact if wrong.
"""

from __future__ import annotations

import pandas as pd


def main() -> None:
    assumptions = pd.read_csv("../data/assumption_register.csv")

    assumptions["assumption_risk_score"] = (
        (1.0 - assumptions["confidence"]) * assumptions["impact_if_wrong"]
    )

    assumptions = assumptions.sort_values("assumption_risk_score", ascending=False)

    print(assumptions)

    assumptions.to_csv("../outputs/assumption_priority_scores.csv", index=False)


if __name__ == "__main__":
    main()
