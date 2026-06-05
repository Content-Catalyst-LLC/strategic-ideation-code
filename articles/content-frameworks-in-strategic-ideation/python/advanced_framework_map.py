#!/usr/bin/env python3
"""
Optional advanced analytics for Content Frameworks in Strategic Ideation.
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

frameworks = pd.read_csv(RAW / "frameworks.csv")
components = pd.read_csv(RAW / "components.csv")
links = pd.read_csv(RAW / "framework_component_links.csv")

frameworks["framework_strength"] = (
    0.10 * frameworks["structure_quality"]
    + 0.10 * frameworks["conceptual_clarity"]
    + 0.11 * frameworks["evidence_discipline"]
    + 0.10 * frameworks["assumption_visibility"]
    + 0.10 * frameworks["narrative_coherence"]
    + 0.12 * frameworks["decision_relevance"]
    + 0.10 * frameworks["modularity"]
    + 0.10 * frameworks["reuse_readiness"]
    + 0.08 * frameworks["governance_strength"]
    + 0.06 * frameworks["ethical_visibility"]
    + 0.03 * frameworks["ai_governance"]
)

frameworks["framework_risk"] = (
    0.10 * (1 - frameworks["structure_quality"])
    + 0.11 * (1 - frameworks["conceptual_clarity"])
    + 0.12 * (1 - frameworks["evidence_discipline"])
    + 0.11 * (1 - frameworks["assumption_visibility"])
    + 0.09 * (1 - frameworks["narrative_coherence"])
    + 0.12 * (1 - frameworks["decision_relevance"])
    + 0.09 * (1 - frameworks["modularity"])
    + 0.09 * (1 - frameworks["reuse_readiness"])
    + 0.08 * (1 - frameworks["governance_strength"])
    + 0.06 * (1 - frameworks["ethical_visibility"])
    + 0.03 * (1 - frameworks["ai_governance"])
)

frameworks.sort_values("framework_strength", ascending=True).plot(
    kind="barh",
    x="framework_name",
    y="framework_strength",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Framework strength")
plt.ylabel("Framework")
plt.title("Strategic Content Framework Strength")
plt.tight_layout()
plt.savefig(FIGURES / "framework_strength.png", dpi=160)
plt.close()

frameworks.sort_values("framework_risk", ascending=True).plot(
    kind="barh",
    x="framework_name",
    y="framework_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Framework risk")
plt.ylabel("Framework")
plt.title("Strategic Content Framework Risk")
plt.tight_layout()
plt.savefig(FIGURES / "framework_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    frameworks["framework_risk"],
    frameworks["framework_strength"],
    s=frameworks["reuse_readiness"] * 420,
)
for _, row in frameworks.iterrows():
    plt.annotate(row["framework_id"], (row["framework_risk"], row["framework_strength"]))
plt.xlabel("Framework risk")
plt.ylabel("Framework strength")
plt.title("Framework Risk and Reuse Readiness")
plt.tight_layout()
plt.savefig(FIGURES / "framework_risk_reuse_map.png", dpi=160)
plt.close()

graph = nx.DiGraph()

for _, row in frameworks.iterrows():
    graph.add_node(
        row["framework_id"],
        label=row["framework_name"],
        node_type="framework",
        score=float(row["framework_strength"]),
    )

for _, row in components.iterrows():
    graph.add_node(
        row["component_id"],
        label=row["component_name"],
        node_type="component",
        score=float(row["reuse_value"]),
    )

for _, row in links.iterrows():
    graph.add_edge(
        row["framework_id"],
        row["component_id"],
        relation=row["relationship_type"],
        weight=float(row["importance"]),
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

centrality_table.to_csv(TABLES / "framework_map_centrality.csv", index=False)

plt.figure(figsize=(13, 9))
pos = nx.spring_layout(graph, seed=42)
nx.draw_networkx_nodes(graph, pos, node_size=900)
nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>")
nx.draw_networkx_labels(graph, pos, labels={node: node for node in graph.nodes()}, font_size=9)
edge_labels = nx.get_edge_attributes(graph, "relation")
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=7)
plt.title("Strategic Content Framework Map")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_content_framework_map.png", dpi=160)
plt.close()

frameworks.to_csv(TABLES / "advanced_framework_scores.csv", index=False)
components.to_csv(TABLES / "content_framework_components.csv", index=False)
links.to_csv(TABLES / "content_framework_relationships.csv", index=False)

print("Advanced framework mapping complete.")
print(f"Wrote: {FIGURES / 'framework_strength.png'}")
print(f"Wrote: {FIGURES / 'framework_risk.png'}")
print(f"Wrote: {FIGURES / 'framework_risk_reuse_map.png'}")
print(f"Wrote: {FIGURES / 'strategic_content_framework_map.png'}")
print(f"Wrote: {TABLES / 'framework_map_centrality.csv'}")
