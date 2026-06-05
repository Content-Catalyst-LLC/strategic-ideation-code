#!/usr/bin/env python3
"""
Optional advanced analytics for Strategic Communication and Conceptual Coherence.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"

FIGURES.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import networkx as nx
except ImportError as exc:
    print("Missing optional advanced analytics dependencies.")
    print("Run:")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install -r python/requirements-advanced.txt")
    raise SystemExit(1) from exc

profiles = pd.read_csv(RAW / "communication_profiles.csv")
concepts = pd.read_csv(RAW / "concepts.csv")
claims = pd.read_csv(RAW / "claim_evidence.csv")

profiles["coherence_strength"] = (
    0.11 * profiles["concept_definition"]
    + 0.11 * profiles["narrative_coherence"]
    + 0.13 * profiles["evidence_integrity"]
    + 0.10 * profiles["audience_adaptation"]
    + 0.13 * profiles["decision_alignment"]
    + 0.11 * profiles["implementation_translatability"]
    + 0.08 * profiles["feedback_quality"]
    + 0.10 * profiles["governance_strength"]
    + 0.09 * profiles["ethical_visibility"]
    + 0.04 * profiles["ai_governance"]
)

profiles["meaning_loss_risk"] = (
    0.12 * (1 - profiles["concept_definition"])
    + 0.10 * (1 - profiles["narrative_coherence"])
    + 0.13 * (1 - profiles["evidence_integrity"])
    + 0.10 * (1 - profiles["audience_adaptation"])
    + 0.13 * (1 - profiles["decision_alignment"])
    + 0.11 * (1 - profiles["implementation_translatability"])
    + 0.08 * (1 - profiles["feedback_quality"])
    + 0.09 * (1 - profiles["governance_strength"])
    + 0.10 * (1 - profiles["ethical_visibility"])
    + 0.04 * (1 - profiles["ai_governance"])
)

profiles.sort_values("coherence_strength", ascending=True).plot(
    kind="barh",
    x="communication_profile",
    y="coherence_strength",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Coherence strength")
plt.ylabel("Communication profile")
plt.title("Strategic Communication Coherence Strength")
plt.tight_layout()
plt.savefig(FIGURES / "communication_coherence_strength.png", dpi=160)
plt.close()

profiles.sort_values("meaning_loss_risk", ascending=True).plot(
    kind="barh",
    x="communication_profile",
    y="meaning_loss_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Meaning loss risk")
plt.ylabel("Communication profile")
plt.title("Strategic Meaning Loss Risk")
plt.tight_layout()
plt.savefig(FIGURES / "meaning_loss_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    profiles["meaning_loss_risk"],
    profiles["coherence_strength"],
    s=profiles["ethical_visibility"] * 420,
)
for _, row in profiles.iterrows():
    plt.annotate(row["profile_id"], (row["meaning_loss_risk"], row["coherence_strength"]))
plt.xlabel("Meaning loss risk")
plt.ylabel("Coherence strength")
plt.title("Meaning Loss Risk and Conceptual Coherence")
plt.tight_layout()
plt.savefig(FIGURES / "meaning_loss_coherence_map.png", dpi=160)
plt.close()

# Build a simple communication coherence graph.
graph = nx.DiGraph()

for _, row in profiles.iterrows():
    graph.add_node(
        row["profile_id"],
        label=row["communication_profile"],
        node_type="profile",
        score=float(row["coherence_strength"]),
    )

for _, row in concepts.iterrows():
    graph.add_node(
        row["concept_id"],
        label=row["concept_name"],
        node_type="concept",
        score=float(row["definition_quality"]),
    )

for _, row in claims.iterrows():
    graph.add_node(
        row["claim_id"],
        label=row["claim_type"],
        node_type="claim",
        score=float(row["evidence_quality"]),
    )
    graph.add_edge(row["profile_id"], row["claim_id"], relation="makes_claim", weight=float(row["confidence_level"]))

# Synthetic concept-profile links for demonstration.
concept_links = [
    ("SC001", "C001", "communicates"),
    ("SC002", "C001", "translates"),
    ("SC003", "C003", "communicates"),
    ("SC004", "C005", "frames"),
    ("SC005", "C004", "risks_flattening"),
    ("SC006", "C002", "preserves"),
    ("SC007", "C005", "aligns"),
    ("SC008", "C004", "updates"),
]
for source, target, relation in concept_links:
    graph.add_edge(source, target, relation=relation, weight=0.7)

centrality = nx.degree_centrality(graph)
centrality_table = pd.DataFrame([
    {
        "node_id": node,
        "label": graph.nodes[node]["label"],
        "node_type": graph.nodes[node]["node_type"],
        "degree_centrality": score,
        "score": graph.nodes[node]["score"],
    }
    for node, score in centrality.items()
]).sort_values("degree_centrality", ascending=False)

centrality_table.to_csv(TABLES / "coherence_graph_centrality.csv", index=False)

plt.figure(figsize=(13, 9))
pos = nx.spring_layout(graph, seed=42)
nx.draw_networkx_nodes(graph, pos, node_size=850)
nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>")
nx.draw_networkx_labels(graph, pos, labels={node: node for node in graph.nodes()}, font_size=8)
edge_labels = nx.get_edge_attributes(graph, "relation")
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=7)
plt.title("Strategic Communication and Conceptual Coherence Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_communication_coherence_graph.png", dpi=160)
plt.close()

profiles.to_csv(TABLES / "advanced_communication_profile_scores.csv", index=False)
concepts.to_csv(TABLES / "concept_definition_review.csv", index=False)
claims.to_csv(TABLES / "claim_evidence_review.csv", index=False)

print("Advanced coherence graph analytics complete.")
print(f"Wrote: {FIGURES / 'communication_coherence_strength.png'}")
print(f"Wrote: {FIGURES / 'meaning_loss_risk.png'}")
print(f"Wrote: {FIGURES / 'meaning_loss_coherence_map.png'}")
print(f"Wrote: {FIGURES / 'strategic_communication_coherence_graph.png'}")
print(f"Wrote: {TABLES / 'coherence_graph_centrality.csv'}")
