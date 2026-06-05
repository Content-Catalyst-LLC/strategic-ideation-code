#!/usr/bin/env python3
"""
Optional advanced analytics for Knowledge Architecture in Strategic Ideation.
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

ideas = pd.read_csv(RAW / "idea_records.csv")
edges = pd.read_csv(RAW / "relationships.csv")

ideas["architecture_strength"] = (
    0.11 * ideas["taxonomy_quality"]
    + 0.12 * ideas["metadata_completeness"]
    + 0.11 * ideas["semantic_clarity"]
    + 0.12 * ideas["evidence_linkage"]
    + 0.11 * ideas["assumption_clarity"]
    + 0.11 * ideas["relationship_mapping"]
    + 0.12 * ideas["retrieval_readiness"]
    + 0.09 * ideas["decision_memory"]
    + 0.07 * ideas["stewardship_quality"]
    + 0.04 * ideas["ethical_representation"]
)

ideas["architecture_risk"] = (
    0.11 * (1 - ideas["taxonomy_quality"])
    + 0.12 * (1 - ideas["metadata_completeness"])
    + 0.12 * (1 - ideas["semantic_clarity"])
    + 0.13 * (1 - ideas["evidence_linkage"])
    + 0.12 * (1 - ideas["assumption_clarity"])
    + 0.10 * (1 - ideas["relationship_mapping"])
    + 0.12 * (1 - ideas["retrieval_readiness"])
    + 0.09 * (1 - ideas["decision_memory"])
    + 0.06 * (1 - ideas["stewardship_quality"])
    + 0.03 * (1 - ideas["ethical_representation"])
)

ideas.sort_values("architecture_strength", ascending=True).plot(
    kind="barh",
    x="idea_title",
    y="architecture_strength",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Architecture strength")
plt.ylabel("Strategic idea")
plt.title("Strategic Idea Architecture Strength")
plt.tight_layout()
plt.savefig(FIGURES / "idea_architecture_strength.png", dpi=160)
plt.close()

ideas.sort_values("architecture_risk", ascending=True).plot(
    kind="barh",
    x="idea_title",
    y="architecture_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Architecture risk")
plt.ylabel("Strategic idea")
plt.title("Strategic Knowledge Architecture Risk")
plt.tight_layout()
plt.savefig(FIGURES / "idea_architecture_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["architecture_risk"],
    ideas["architecture_strength"],
    s=ideas["retrieval_readiness"] * 420,
)
for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["architecture_risk"], row["architecture_strength"]))
plt.xlabel("Architecture risk")
plt.ylabel("Architecture strength")
plt.title("Architecture Risk and Strategic Reuse Potential")
plt.tight_layout()
plt.savefig(FIGURES / "architecture_risk_reuse_map.png", dpi=160)
plt.close()

graph = nx.DiGraph()

for _, row in ideas.iterrows():
    graph.add_node(
        row["idea_id"],
        label=row["idea_title"],
        node_type="idea",
        domain=row["domain"],
        architecture_strength=float(row["architecture_strength"]),
    )

for _, row in edges.iterrows():
    graph.add_edge(
        row["source_id"],
        row["target_id"],
        relation=row["relationship_type"],
        weight=float(row["relationship_strength"]),
    )

centrality = nx.degree_centrality(graph)
in_degree = dict(graph.in_degree())
out_degree = dict(graph.out_degree())

centrality_table = pd.DataFrame([
    {
        "idea_id": node,
        "idea_title": graph.nodes[node]["label"],
        "domain": graph.nodes[node]["domain"],
        "degree_centrality": score,
        "in_degree": in_degree[node],
        "out_degree": out_degree[node],
        "architecture_strength": graph.nodes[node]["architecture_strength"],
    }
    for node, score in centrality.items()
]).sort_values("degree_centrality", ascending=False)

centrality_table.to_csv(TABLES / "knowledge_graph_centrality.csv", index=False)

plt.figure(figsize=(12, 9))
pos = nx.spring_layout(graph, seed=42)
nx.draw_networkx_nodes(graph, pos, node_size=900)
nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>")
nx.draw_networkx_labels(graph, pos, labels={node: node for node in graph.nodes()}, font_size=9)
edge_labels = nx.get_edge_attributes(graph, "relation")
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=7)
plt.title("Strategic Idea Knowledge Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_idea_knowledge_graph.png", dpi=160)
plt.close()

ideas.to_csv(TABLES / "advanced_idea_architecture_scores.csv", index=False)
edges.to_csv(TABLES / "strategic_idea_relationships.csv", index=False)

print("Advanced knowledge graph analytics complete.")
print(f"Wrote: {FIGURES / 'idea_architecture_strength.png'}")
print(f"Wrote: {FIGURES / 'idea_architecture_risk.png'}")
print(f"Wrote: {FIGURES / 'architecture_risk_reuse_map.png'}")
print(f"Wrote: {FIGURES / 'strategic_idea_knowledge_graph.png'}")
print(f"Wrote: {TABLES / 'knowledge_graph_centrality.csv'}")
