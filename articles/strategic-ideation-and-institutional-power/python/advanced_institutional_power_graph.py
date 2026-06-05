#!/usr/bin/env python3
"""
Optional advanced analytics for Strategic Ideation and Institutional Power.
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

ideas = pd.read_csv(RAW / "power_ideas.csv")

ideas["merit_score"] = (
    0.28 * ideas["strategic_merit"]
    + 0.21 * ideas["evidence_strength"]
    + 0.16 * ideas["stakeholder_influence"]
    + 0.13 * ideas["dissent_protection"]
    + 0.12 * ideas["classification_visibility"]
    + 0.10 * ideas["ethical_visibility"]
)
ideas["institutional_support"] = (
    0.28 * ideas["executive_sponsorship"]
    + 0.24 * ideas["resource_fit"]
    + 0.24 * ideas["power_alignment"]
    + 0.24 * ideas["advancement_likelihood"]
)
ideas["power_distortion"] = ideas["institutional_support"] - ideas["merit_score"]
ideas["voice_gap"] = ideas["advancement_likelihood"] - ideas["stakeholder_influence"]

ideas.sort_values("power_distortion", ascending=True).plot(
    kind="barh",
    x="idea",
    y="power_distortion",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Power distortion: institutional support minus merit")
plt.ylabel("Strategic idea")
plt.title("Power Distortion in Strategic Idea Advancement")
plt.tight_layout()
plt.savefig(FIGURES / "power_distortion.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["merit_score"],
    ideas["institutional_support"],
    s=ideas["power_alignment"] * 420,
)
for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["merit_score"], row["institutional_support"]))
plt.xlabel("Merit score")
plt.ylabel("Institutional support")
plt.title("Strategic Merit and Institutional Support")
plt.tight_layout()
plt.savefig(FIGURES / "merit_vs_institutional_support.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["stakeholder_influence"],
    ideas["advancement_likelihood"],
    s=ideas["executive_sponsorship"] * 420,
)
for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["stakeholder_influence"], row["advancement_likelihood"]))
plt.xlabel("Stakeholder influence")
plt.ylabel("Advancement likelihood")
plt.title("Voice Gap in Strategic Idea Advancement")
plt.tight_layout()
plt.savefig(FIGURES / "voice_gap_map.png", dpi=160)
plt.close()

graph = nx.DiGraph()

for _, row in ideas.iterrows():
    graph.add_node(row["idea_id"], label=row["idea"], node_type="idea", score=float(row["power_distortion"]))

dimension_nodes = {
    "authority:Executive Sponsorship": "executive_sponsorship",
    "resource:Resource Fit": "resource_fit",
    "power:Power Alignment": "power_alignment",
    "stakeholder:Stakeholder Influence": "stakeholder_influence",
    "dissent:Dissent Protection": "dissent_protection",
    "evidence:Evidence Strength": "evidence_strength",
    "classification:Classification Visibility": "classification_visibility",
}

for node_id, column in dimension_nodes.items():
    label = node_id.split(":", 1)[1]
    node_type = node_id.split(":", 1)[0]
    graph.add_node(node_id, label=label, node_type=node_type, score=1.0)
    for _, row in ideas.iterrows():
        relation = "supports_advancement" if column in ["executive_sponsorship", "resource_fit", "power_alignment"] else "checks_power"
        graph.add_edge(node_id, row["idea_id"], relation=relation, weight=float(row[column]))

# Add selected institutional relationships.
relationships = [
    ("PI002", "PI004", "shares_power_aligned_technology_logic", 0.70),
    ("PI006", "PI002", "shares_efficiency_narrative", 0.74),
    ("PI001", "PI005", "shares_accountability_governance_logic", 0.78),
    ("PI003", "PI007", "shares_learning_and_memory_logic", 0.76),
    ("PI008", "PI005", "requires_long_term_voice_and_accountability", 0.72),
    ("PI004", "PI006", "requires_burden_review", 0.80),
]
for source, target, relation, weight in relationships:
    graph.add_edge(source, target, relation=relation, weight=weight)

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

centrality_table.to_csv(TABLES / "institutional_power_graph_centrality.csv", index=False)

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
plt.title("Institutional Power Graph Around Strategic Ideas")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "institutional_power_graph.png", dpi=160)
plt.close()

ideas.to_csv(TABLES / "advanced_power_idea_scores.csv", index=False)

print("Advanced institutional power graph analytics complete.")
print(f"Wrote: {FIGURES / 'power_distortion.png'}")
print(f"Wrote: {FIGURES / 'merit_vs_institutional_support.png'}")
print(f"Wrote: {FIGURES / 'voice_gap_map.png'}")
print(f"Wrote: {FIGURES / 'institutional_power_graph.png'}")
print(f"Wrote: {TABLES / 'institutional_power_graph_centrality.csv'}")
