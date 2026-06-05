#!/usr/bin/env python3
"""
Optional advanced analytics for Taxonomy of Strategic Ideas.
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

records = pd.read_csv(RAW / "taxonomy_records.csv")
relationships = pd.read_csv(RAW / "idea_relationships.csv")

records["taxonomy_strength"] = (
    0.12 * records["category_clarity"]
    + 0.10 * records["level_fit"]
    + 0.10 * records["maturity_accuracy"]
    + 0.12 * records["evidence_classification"]
    + 0.12 * records["function_clarity"]
    + 0.10 * records["relationship_mapping"]
    + 0.12 * records["retrieval_value"]
    + 0.09 * records["governance_strength"]
    + 0.08 * records["ethical_visibility"]
    + 0.05 * records["ai_classification_quality"]
)

records["taxonomy_risk"] = (
    0.12 * (1 - records["category_clarity"])
    + 0.10 * (1 - records["level_fit"])
    + 0.10 * (1 - records["maturity_accuracy"])
    + 0.12 * (1 - records["evidence_classification"])
    + 0.12 * (1 - records["function_clarity"])
    + 0.10 * (1 - records["relationship_mapping"])
    + 0.12 * (1 - records["retrieval_value"])
    + 0.09 * (1 - records["governance_strength"])
    + 0.08 * (1 - records["ethical_visibility"])
    + 0.05 * (1 - records["ai_classification_quality"])
)

records.sort_values("taxonomy_strength", ascending=True).plot(
    kind="barh",
    x="idea_record",
    y="taxonomy_strength",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Taxonomy strength")
plt.ylabel("Idea record")
plt.title("Strategic Idea Taxonomy Strength")
plt.tight_layout()
plt.savefig(FIGURES / "taxonomy_strength.png", dpi=160)
plt.close()

records.sort_values("taxonomy_risk", ascending=True).plot(
    kind="barh",
    x="idea_record",
    y="taxonomy_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Taxonomy risk")
plt.ylabel("Idea record")
plt.title("Strategic Idea Taxonomy Risk")
plt.tight_layout()
plt.savefig(FIGURES / "taxonomy_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    records["taxonomy_risk"],
    records["taxonomy_strength"],
    s=records["retrieval_value"] * 420,
)
for _, row in records.iterrows():
    plt.annotate(row["record_id"], (row["taxonomy_risk"], row["taxonomy_strength"]))
plt.xlabel("Taxonomy risk")
plt.ylabel("Taxonomy strength")
plt.title("Taxonomy Risk and Retrieval Value")
plt.tight_layout()
plt.savefig(FIGURES / "taxonomy_risk_retrieval_map.png", dpi=160)
plt.close()

graph = nx.DiGraph()

for _, row in records.iterrows():
    graph.add_node(row["record_id"], label=row["idea_record"], node_type="idea", score=float(row["taxonomy_strength"]))

taxonomy_fields = ["idea_type", "strategic_level", "maturity_state", "evidence_status", "strategic_function"]
for _, row in records.iterrows():
    for field in taxonomy_fields:
        node_id = f"{field}:{row[field]}"
        graph.add_node(node_id, label=row[field], node_type=field, score=1.0)
        graph.add_edge(row["record_id"], node_id, relation=f"classified_as_{field}", weight=1.0)

for _, row in relationships.iterrows():
    graph.add_edge(
        row["source_record"],
        row["target_record"],
        relation=row["relationship_type"],
        weight=float(row["strategic_importance"]),
    )

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

centrality_table.to_csv(TABLES / "taxonomy_graph_centrality.csv", index=False)

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(graph, seed=42)
nx.draw_networkx_nodes(graph, pos, node_size=800)
nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>")
nx.draw_networkx_labels(
    graph,
    pos,
    labels={node: node if graph.nodes[node]["node_type"] == "idea" else graph.nodes[node]["label"] for node in graph.nodes()},
    font_size=7,
)
edge_labels = nx.get_edge_attributes(graph, "relation")
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)
plt.title("Strategic Idea Taxonomy Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_idea_taxonomy_graph.png", dpi=160)
plt.close()

records.to_csv(TABLES / "advanced_taxonomy_record_scores.csv", index=False)
relationships.to_csv(TABLES / "taxonomy_relationships.csv", index=False)

print("Advanced taxonomy graph analytics complete.")
print(f"Wrote: {FIGURES / 'taxonomy_strength.png'}")
print(f"Wrote: {FIGURES / 'taxonomy_risk.png'}")
print(f"Wrote: {FIGURES / 'taxonomy_risk_retrieval_map.png'}")
print(f"Wrote: {FIGURES / 'strategic_idea_taxonomy_graph.png'}")
print(f"Wrote: {TABLES / 'taxonomy_graph_centrality.csv'}")
