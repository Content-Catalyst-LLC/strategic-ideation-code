"""
Strategic Ideation: Strategic Fit Similarity

Educational example using vector similarity to approximate alignment between
ideas and strategic goals.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


GOAL_VECTOR = np.array([0.82, 0.88, 0.70, 0.82])


def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    """Return cosine similarity between two vectors."""
    denominator = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)

    if denominator == 0:
        return 0.0

    return float(np.dot(vector_a, vector_b) / denominator)


def main() -> None:
    vectors = pd.read_csv("../data/idea_vectors.csv")

    fit_rows = []

    for _, row in vectors.iterrows():
        idea_vector = np.array([
            row["systems_depth"],
            row["public_value"],
            row["implementation_capacity"],
            row["learning_value"]
        ])

        fit_rows.append({
            "idea": row["idea"],
            "strategic_fit_similarity": cosine_similarity(idea_vector, GOAL_VECTOR)
        })

    fit_df = pd.DataFrame(fit_rows).sort_values("strategic_fit_similarity", ascending=False)

    print(fit_df)

    fit_df.to_csv("../outputs/strategic_fit_similarity.csv", index=False)


if __name__ == "__main__":
    main()
