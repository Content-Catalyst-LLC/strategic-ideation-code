#!/usr/bin/env python3
"""
Optional advanced analytics for Institutional Memory and Idea Systems.
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

systems = pd.read_csv(RAW / "memory_systems.csv")
ideas = pd.read_csv(RAW / "idea_lifecycle.csv")
decisions = pd.read_csv(RAW / "decision_memory.csv")
learning = pd.read_csv(RAW / "learning_updates.csv")

systems["memory_strength"] = (
    0.09 * systems["capture_quality"]
    + 0.11 * systems["metadata_completeness"]
    + 0.11 * systems["context_preservation"]
    + 0.13 * systems["decision_memory"]
    + 0.12 * systems["learning_integration"]
    + 0.12 * systems["retrieval_readiness"]
    + 0.10 * systems["reuse_potential"]
    + 0.08 * systems["stewardship_quality"]
    + 0.06 * systems["continuity_resilience"]
    + 0.05 * systems["ethical_memory"]
    + 0.03 * systems["ai_governance"]
)

systems["memory_failure_risk"] = (
    0.09 * (1 - systems["capture_quality"])
    + 0.11 * (1 - systems["metadata_completeness"])
    + 0.11 * (1 - systems["context_preservation"])
    + 0.13 * (1 - systems["decision_memory"])
    + 0.12 * (1 - systems["learning_integration"])
    + 0.12 * (1 - systems["retrieval_readiness"])
    + 0.09 * (1 - systems["reuse_potential"])
    + 0.08 * (1 - systems["stewardship_quality"])
    + 0.07 * (1 - systems["continuity_resilience"])
    + 0.05 * (1 - systems["ethical_memory"])
    + 0.03 * (1 - systems["ai_governance"])
)

systems.sort_values("memory_strength", ascending=True).plot(
    kind="barh",
    x="system_area",
    y="memory_strength",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Memory strength")
plt.ylabel("System area")
plt.title("Institutional Idea Memory Strength")
plt.tight_layout()
plt.savefig(FIGURES / "institutional_memory_strength.png", dpi=160)
plt.close()

systems.sort_values("memory_failure_risk", ascending=True).plot(
    kind="barh",
    x="system_area",
    y="memory_failure_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Memory failure risk")
plt.ylabel("System area")
plt.title("Institutional Memory Failure Risk")
plt.tight_layout()
plt.savefig(FIGURES / "memory_failure_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    systems["memory_failure_risk"],
    systems["memory_strength"],
    s=systems["reuse_potential"] * 420,
)
for _, row in systems.iterrows():
    plt.annotate(row["system_id"], (row["memory_failure_risk"], row["memory_strength"]))
plt.xlabel("Memory failure risk")
plt.ylabel("Memory strength")
plt.title("Memory Failure Risk and Strategic Reuse Potential")
plt.tight_layout()
plt.savefig(FIGURES / "memory_risk_reuse_map.png", dpi=160)
plt.close()

# Build an idea-system graph.
graph = nx.DiGraph()

for _, row in ideas.iterrows():
    graph.add_node(
        row["idea_id"],
        label=row["idea_title"],
        node_type="idea",
        stage=row["lifecycle_stage"],
        score=float(row["evidence_level"]),
    )

for _, row in decisions.iterrows():
    graph.add_node(
        row["decision_id"],
        label=row["decision_type"],
        node_type="decision",
        score=float(row["traceability_quality"]),
    )
    graph.add_edge(row["idea_id"], row["decision_id"], relation="has_decision", weight=float(row["traceability_quality"]))

for _, row in learning.iterrows():
    graph.add_node(
        row["learning_id"],
        label=row["learning_source"],
        node_type="learning",
        score=float(row["evidence_quality"]),
    )
    graph.add_edge(row["learning_id"], row["idea_id"], relation="updates_idea", weight=float(row["followup_quality"]))

# Add selected conceptual reuse links.
reuse_edges = [
    ("IL001", "IL005", "shares_stakeholder_memory"),
    ("IL002", "IL004", "feeds_repository"),
    ("IL003", "IL008", "requires_reuse_condition"),
    ("IL004", "IL007", "supports_decision_memory"),
    ("IL006", "IL002", "capacity_dependency"),
    ("IL008", "IL001", "reactivation_reference"),
]
for source, target, relation in reuse_edges:
    if source in graph and target in graph:
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

centrality_table.to_csv(TABLES / "idea_system_graph_centrality.csv", index=False)

plt.figure(figsize=(13, 9))
pos = nx.spring_layout(graph, seed=42)
nx.draw_networkx_nodes(graph, pos, node_size=850)
nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>")
nx.draw_networkx_labels(graph, pos, labels={node: node for node in graph.nodes()}, font_size=8)
edge_labels = nx.get_edge_attributes(graph, "relation")
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=7)
plt.title("Institutional Memory and Idea System Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURES / "institutional_memory_idea_system_graph.png", dpi=160)
plt.close()

systems.to_csv(TABLES / "advanced_memory_system_scores.csv", index=False)
ideas.to_csv(TABLES / "idea_lifecycle_review.csv", index=False)
decisions.to_csv(TABLES / "decision_memory_review.csv", index=False)
learning.to_csv(TABLES / "learning_update_review.csv", index=False)

print("Advanced idea-system graph analytics complete.")
print(f"Wrote: {FIGURES / 'institutional_memory_strength.png'}")
print(f"Wrote: {FIGURES / 'memory_failure_risk.png'}")
print(f"Wrote: {FIGURES / 'memory_risk_reuse_map.png'}")
print(f"Wrote: {FIGURES / 'institutional_memory_idea_system_graph.png'}")
print(f"Wrote: {TABLES / 'idea_system_graph_centrality.csv'}")
