#!/usr/bin/env python3
"""
Optional advanced analytics for Bad Ideas and Strategic Failure.
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

ideas = pd.read_csv(RAW / "bad_ideas.csv")
pathways = pd.read_csv(RAW / "failure_pathways.csv")

ideas["idea_quality"] = (
    0.12 * ideas["problem_frame_integrity"]
    + 0.11 * ideas["mechanism_clarity"]
    + 0.13 * ideas["evidence_quality"]
    + 0.10 * ideas["context_fit"]
    + 0.12 * ideas["implementation_readiness"]
    + 0.10 * ideas["incentive_alignment"]
    + 0.10 * ideas["ethical_visibility"]
    + 0.09 * ideas["strategic_merit"]
    + 0.08 * ideas["learning_design"]
    + 0.05 * ideas["narrative_honesty"]
)
ideas["power_distortion"] = ideas["institutional_support"] - ideas["strategic_merit"]
ideas["failure_risk"] = (
    0.12 * (1 - ideas["problem_frame_integrity"])
    + 0.11 * (1 - ideas["mechanism_clarity"])
    + 0.13 * (1 - ideas["evidence_quality"])
    + 0.10 * (1 - ideas["context_fit"])
    + 0.12 * (1 - ideas["implementation_readiness"])
    + 0.10 * (1 - ideas["incentive_alignment"])
    + 0.10 * (1 - ideas["ethical_visibility"])
    + 0.08 * (1 - ideas["learning_design"])
    + 0.05 * (1 - ideas["narrative_honesty"])
    + 0.05 * ideas["power_distortion"].clip(lower=0)
    + 0.04 * ideas["ai_fluency_risk"]
)

ideas.sort_values("failure_risk", ascending=True).plot(
    kind="barh",
    x="idea",
    y="failure_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Failure risk")
plt.ylabel("Strategic idea")
plt.title("Bad-Idea Failure Risk")
plt.tight_layout()
plt.savefig(FIGURES / "bad_idea_failure_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["idea_quality"],
    ideas["failure_risk"],
    s=(ideas["power_distortion"].clip(lower=0) + 0.1) * 700,
)
for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["idea_quality"], row["failure_risk"]))
plt.xlabel("Idea quality")
plt.ylabel("Failure risk")
plt.title("Idea Quality and Failure Risk")
plt.tight_layout()
plt.savefig(FIGURES / "idea_quality_failure_risk_map.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["evidence_quality"],
    ideas["institutional_support"],
    s=ideas["ai_fluency_risk"] * 450,
)
for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["evidence_quality"], row["institutional_support"]))
plt.xlabel("Evidence quality")
plt.ylabel("Institutional support")
plt.title("Evidence Quality, Institutional Support, and AI Fluency Risk")
plt.tight_layout()
plt.savefig(FIGURES / "evidence_support_ai_fluency_map.png", dpi=160)
plt.close()

graph = nx.DiGraph()

for _, row in ideas.iterrows():
    graph.add_node(row["idea_id"], label=row["idea"], node_type="idea", score=float(row["failure_risk"]))

weakness_nodes = {
    "weakness:Weak Problem Frame": "problem_frame_integrity",
    "weakness:Weak Evidence": "evidence_quality",
    "weakness:Implementation Fantasy": "implementation_readiness",
    "weakness:Incentive Failure": "incentive_alignment",
    "weakness:Hidden Burden": "ethical_visibility",
    "weakness:Weak Learning Design": "learning_design",
    "weakness:Narrative Overreach": "narrative_honesty",
}

for node_id, column in weakness_nodes.items():
    label = node_id.split(":", 1)[1]
    graph.add_node(node_id, label=label, node_type="weakness", score=1.0)
    for _, row in ideas.iterrows():
        weakness = 1 - float(row[column])
        if weakness > 0.35:
            graph.add_edge(row["idea_id"], node_id, relation="has_risk", weight=weakness)

for _, row in pathways.iterrows():
    pathway_node = f"pathway:{row['weakness_type']}"
    graph.add_node(pathway_node, label=row["weakness_type"], node_type="pathway", score=float(row["escalation_risk"]))
    graph.add_edge(row["idea_id"], pathway_node, relation="may_follow_pathway", weight=float(row["escalation_risk"]))

interventions = [
    ("intervention:Problem-Frame Audit", "weakness:Weak Problem Frame", "mitigates"),
    ("intervention:Claim-Evidence Matrix", "weakness:Weak Evidence", "mitigates"),
    ("intervention:Implementation Readiness Review", "weakness:Implementation Fantasy", "mitigates"),
    ("intervention:Incentive Analysis", "weakness:Incentive Failure", "mitigates"),
    ("intervention:Stakeholder Burden Review", "weakness:Hidden Burden", "mitigates"),
    ("intervention:Stop Rules", "weakness:Weak Learning Design", "mitigates"),
    ("intervention:Narrative Honesty Review", "weakness:Narrative Overreach", "mitigates"),
]
for source, target, relation in interventions:
    graph.add_node(source, label=source.split(":", 1)[1], node_type="intervention", score=1.0)
    graph.add_edge(source, target, relation=relation, weight=0.80)

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

centrality_table.to_csv(TABLES / "failure_pathway_graph_centrality.csv", index=False)

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(graph, seed=42)
nx.draw_networkx_nodes(graph, pos, node_size=820)
nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>")
nx.draw_networkx_labels(
    graph,
    pos,
    labels={node: node if graph.nodes[node]["node_type"] == "idea" else graph.nodes[node]["label"] for node in graph.nodes()},
    font_size=7,
)
edge_labels = nx.get_edge_attributes(graph, "relation")
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)
plt.title("Bad Ideas and Strategic Failure Pathway Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "bad_idea_failure_pathway_graph.png", dpi=160)
plt.close()

ideas.to_csv(TABLES / "advanced_bad_idea_scores.csv", index=False)

print("Advanced failure pathway graph analytics complete.")
print(f"Wrote: {FIGURES / 'bad_idea_failure_risk.png'}")
print(f"Wrote: {FIGURES / 'idea_quality_failure_risk_map.png'}")
print(f"Wrote: {FIGURES / 'evidence_support_ai_fluency_map.png'}")
print(f"Wrote: {FIGURES / 'bad_idea_failure_pathway_graph.png'}")
print(f"Wrote: {TABLES / 'failure_pathway_graph_centrality.csv'}")
