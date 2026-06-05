#!/usr/bin/env python3
"""
Optional advanced analytics for Ethics of Strategic Ideation.
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

ideas = pd.read_csv(RAW / "ethical_ideas.csv")
impacts = pd.read_csv(RAW / "stakeholder_impacts.csv")
claims = pd.read_csv(RAW / "claim_evidence_ethics.csv")
accountability = pd.read_csv(RAW / "accountability_redress.csv")

ideas["ethical_legitimacy"] = (
    0.12 * ideas["stakeholder_voice"]
    + 0.12 * ideas["evidence_integrity"]
    + 0.10 * ideas["burden_visibility"]
    + 0.09 * ideas["uncertainty_visibility"]
    + 0.08 * ideas["reversibility"]
    + 0.11 * ideas["long_term_responsibility"]
    + 0.07 * ideas["ai_governance"]
    + 0.09 * ideas["accountability"]
    + 0.07 * ideas["redress_quality"]
    + 0.08 * ideas["problem_frame_integrity"]
    + 0.07 * ideas["power_review"]
)

ideas["ethical_risk"] = (
    0.13 * (1 - ideas["stakeholder_voice"])
    + 0.12 * (1 - ideas["evidence_integrity"])
    + 0.12 * (1 - ideas["burden_visibility"])
    + 0.10 * (1 - ideas["uncertainty_visibility"])
    + 0.09 * (1 - ideas["reversibility"])
    + 0.10 * (1 - ideas["long_term_responsibility"])
    + 0.10 * (1 - ideas["ai_governance"])
    + 0.08 * (1 - ideas["accountability"])
    + 0.07 * (1 - ideas["redress_quality"])
    + 0.05 * (1 - ideas["problem_frame_integrity"])
    + 0.04 * (1 - ideas["power_review"])
)

ideas.sort_values("ethical_legitimacy", ascending=True).plot(
    kind="barh",
    x="idea",
    y="ethical_legitimacy",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Ethical legitimacy")
plt.ylabel("Strategic idea")
plt.title("Ethical Legitimacy of Strategic Ideas")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_legitimacy.png", dpi=160)
plt.close()

ideas.sort_values("ethical_risk", ascending=True).plot(
    kind="barh",
    x="idea",
    y="ethical_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Ethical risk")
plt.ylabel("Strategic idea")
plt.title("Ethical Risk of Strategic Ideas")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["ethical_risk"],
    ideas["ethical_legitimacy"],
    s=ideas["burden_visibility"] * 420,
)
for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["ethical_risk"], row["ethical_legitimacy"]))
plt.xlabel("Ethical risk")
plt.ylabel("Ethical legitimacy")
plt.title("Ethical Risk and Legitimacy in Strategic Ideation")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_risk_legitimacy_map.png", dpi=160)
plt.close()

graph = nx.DiGraph()

for _, row in ideas.iterrows():
    graph.add_node(row["idea_id"], label=row["idea"], node_type="idea", score=float(row["ethical_legitimacy"]))

for _, row in impacts.iterrows():
    stakeholder_node = f"stakeholder:{row['stakeholder_group']}"
    graph.add_node(stakeholder_node, label=row["stakeholder_group"], node_type="stakeholder", score=1.0)
    graph.add_edge(row["idea_id"], stakeholder_node, relation="affects", weight=float(row["risk_exposure"]))
    graph.add_node(row["impact_id"], label=f"impact:{row['stakeholder_group']}", node_type="impact", score=float(row["burden_score"]))
    graph.add_edge(row["impact_id"], row["idea_id"], relation="reviews", weight=float(row["voice_quality"]))
    graph.add_edge(row["impact_id"], stakeholder_node, relation="burdens_or_benefits", weight=float(row["burden_score"]))

for _, row in claims.iterrows():
    graph.add_node(row["claim_id"], label=row["claim_type"], node_type="claim", score=float(row["ethical_salience"]))
    graph.add_edge(row["idea_id"], row["claim_id"], relation="makes_claim", weight=float(row["confidence_level"]))

for _, row in accountability.iterrows():
    accountability_node = f"accountability:{row['idea_id']}"
    graph.add_node(accountability_node, label="accountability_redress", node_type="accountability", score=float(row["redress_access"]))
    graph.add_edge(row["idea_id"], accountability_node, relation="requires_redress", weight=float(row["redress_access"]))

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

centrality_table.to_csv(TABLES / "ethical_impact_graph_centrality.csv", index=False)

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
plt.title("Ethical Stakeholder Impact Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_stakeholder_impact_graph.png", dpi=160)
plt.close()

ideas.to_csv(TABLES / "advanced_ethical_idea_scores.csv", index=False)
impacts.to_csv(TABLES / "advanced_stakeholder_impacts.csv", index=False)
claims.to_csv(TABLES / "advanced_claim_evidence_ethics.csv", index=False)

print("Advanced ethical impact graph analytics complete.")
print(f"Wrote: {FIGURES / 'ethical_legitimacy.png'}")
print(f"Wrote: {FIGURES / 'ethical_risk.png'}")
print(f"Wrote: {FIGURES / 'ethical_risk_legitimacy_map.png'}")
print(f"Wrote: {FIGURES / 'ethical_stakeholder_impact_graph.png'}")
print(f"Wrote: {TABLES / 'ethical_impact_graph_centrality.csv'}")
