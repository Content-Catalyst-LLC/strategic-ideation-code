#!/usr/bin/env python3
"""
Optional advanced analytics for Future Directions in Strategic Ideation.
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

ideas = pd.read_csv(RAW / "future_ideas.csv")
scenarios = pd.read_csv(RAW / "scenario_options.csv")
ai = pd.read_csv(RAW / "ai_governance.csv")
ci = pd.read_csv(RAW / "collective_intelligence.csv")
learning = pd.read_csv(RAW / "learning_memory.csv")

ideas["future_ready_score"] = (
    0.10 * ideas["problem_frame_quality"]
    + 0.10 * ideas["evidence_quality"]
    + 0.10 * ideas["adaptability"]
    + 0.11 * ideas["scenario_robustness"]
    + 0.10 * ideas["stakeholder_legitimacy"]
    + 0.09 * ideas["implementation_readiness"]
    + 0.10 * ideas["ethical_visibility"]
    + 0.11 * ideas["learning_design"]
    + 0.08 * ideas["option_value"]
    + 0.06 * ideas["ai_governance"]
    + 0.05 * ideas["systems_responsibility"]
)
ideas["future_risk"] = 1 - ideas["future_ready_score"]

ideas.sort_values("future_ready_score", ascending=True).plot(
    kind="barh",
    x="idea",
    y="future_ready_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Future-ready score")
plt.ylabel("Strategic idea")
plt.title("Future-Ready Strategic Idea Scores")
plt.tight_layout()
plt.savefig(FIGURES / "future_ready_scores.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["scenario_robustness"],
    ideas["learning_design"],
    s=ideas["option_value"] * 450,
)
for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["scenario_robustness"], row["learning_design"]))
plt.xlabel("Scenario robustness")
plt.ylabel("Learning design")
plt.title("Scenario Robustness, Learning Design, and Option Value")
plt.tight_layout()
plt.savefig(FIGURES / "scenario_learning_option_map.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["stakeholder_legitimacy"],
    ideas["ethical_visibility"],
    s=ideas["systems_responsibility"] * 450,
)
for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["stakeholder_legitimacy"], row["ethical_visibility"]))
plt.xlabel("Stakeholder legitimacy")
plt.ylabel("Ethical visibility")
plt.title("Legitimacy, Ethics, and Systems Responsibility")
plt.tight_layout()
plt.savefig(FIGURES / "legitimacy_ethics_systems_map.png", dpi=160)
plt.close()

graph = nx.DiGraph()

for _, row in ideas.iterrows():
    graph.add_node(row["idea_id"], label=row["idea"], node_type="idea", score=float(row["future_ready_score"]))

for _, row in scenarios.iterrows():
    node = f"scenario:{row['scenario']}"
    graph.add_node(node, label=row["scenario"], node_type="scenario", score=float(row["scenario_performance"]))
    graph.add_edge(row["idea_id"], node, relation="stress_tested_against", weight=float(row["scenario_performance"]))

for _, row in ai.iterrows():
    node = f"ai:{row['ai_use_case']}"
    graph.add_node(node, label=row["ai_use_case"], node_type="ai_governance", score=float(row["fluency_risk"]))
    graph.add_edge(row["idea_id"], node, relation="requires_ai_review", weight=float(row["ai_risk"]) if "ai_risk" in row else float(row["fluency_risk"]))

for _, row in ci.iterrows():
    node = f"collective:{row['knowledge_source']}"
    graph.add_node(node, label=row["knowledge_source"], node_type="collective_intelligence", score=float(row["synthesis_quality"]))
    graph.add_edge(row["idea_id"], node, relation="uses_collective_knowledge", weight=float(row["synthesis_quality"]))

for _, row in learning.iterrows():
    node = f"learning:{row['lm_id']}"
    graph.add_node(node, label="learning_memory_record", node_type="learning", score=float(row["decision_memory_quality"]))
    graph.add_edge(row["idea_id"], node, relation="preserves_learning", weight=float(row["decision_memory_quality"]))

capabilities = {
    "capability:Scenario Planning": ["FI002", "FI004", "FI008"],
    "capability:AI Governance": ["FI001", "FI005"],
    "capability:Knowledge Architecture": ["FI001", "FI006"],
    "capability:Democratic Participation": ["FI003", "FI007"],
    "capability:Systems Resilience": ["FI004", "FI008"],
    "capability:Adaptive Learning": ["FI002", "FI006", "FI008"],
}

for capability, linked_ideas in capabilities.items():
    label = capability.split(":", 1)[1]
    graph.add_node(capability, label=label, node_type="capability", score=1.0)
    for idea_id in linked_ideas:
        graph.add_edge(capability, idea_id, relation="enables", weight=0.80)

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

centrality_table.to_csv(TABLES / "future_ideation_system_centrality.csv", index=False)

plt.figure(figsize=(15, 11))
pos = nx.spring_layout(graph, seed=42)
nx.draw_networkx_nodes(graph, pos, node_size=780)
nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>")
nx.draw_networkx_labels(
    graph,
    pos,
    labels={node: node if graph.nodes[node]["node_type"] == "idea" else graph.nodes[node]["label"] for node in graph.nodes()},
    font_size=7,
)
edge_labels = nx.get_edge_attributes(graph, "relation")
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)
plt.title("Future-Ready Strategic Ideation System Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "future_ideation_system_graph.png", dpi=160)
plt.close()

ideas.to_csv(TABLES / "advanced_future_ready_idea_scores.csv", index=False)

print("Advanced future ideation system graph analytics complete.")
print(f"Wrote: {FIGURES / 'future_ready_scores.png'}")
print(f"Wrote: {FIGURES / 'scenario_learning_option_map.png'}")
print(f"Wrote: {FIGURES / 'legitimacy_ethics_systems_map.png'}")
print(f"Wrote: {FIGURES / 'future_ideation_system_graph.png'}")
print(f"Wrote: {TABLES / 'future_ideation_system_centrality.csv'}")
