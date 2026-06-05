#!/usr/bin/env python3
from pathlib import Path
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Missing optional advanced analytics dependencies.")
    print("Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r python/requirements-advanced.txt")
    raise SystemExit(1) from exc

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"
TABLES.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

options = pd.read_csv(RAW / "strategic_options.csv")
options["option_value_score"] = (0.10*options["initial_return"]+0.17*options["learning_value"]+0.17*options["flexibility"]+0.12*options["reversibility"]+0.11*options["scalability"]+0.13*options["modularity"]-0.14*options["lock_in_exposure"]-0.06*options["carrying_cost"]+0.11*options["governance_readiness"]+0.09*options["ethical_resilience"])
options["lock_in_warning"] = (0.30*options["lock_in_exposure"]+0.18*(1-options["reversibility"])+0.16*(1-options["flexibility"])+0.14*(1-options["modularity"])+0.12*(1-options["governance_readiness"])+0.10*(1-options["ethical_resilience"]))
for col, title, filename in [("option_value_score","Strategic Option Value Score","option_value_scores.png"),("lock_in_warning","Lock-In Warning","lock_in_warning.png")]:
    options.sort_values(col, ascending=True).plot(kind="barh", x="option_name", y=col, legend=False, figsize=(12,8))
    plt.title(title); plt.xlabel(col.replace("_"," ")); plt.ylabel("Option"); plt.tight_layout(); plt.savefig(FIGURES / filename, dpi=160); plt.close()

scenarios = pd.read_csv(RAW / "scenario_options.csv")
scenario_cols = ["stable_growth","market_shift","regulatory_change","technology_disruption","stakeholder_resistance","cost_shock","implementation_delay","system_stress"]
scenarios = scenarios.merge(options[["option_id","option_name"]], on="option_id", how="left")
long = scenarios.melt(id_vars=["option_name"], value_vars=scenario_cols, var_name="scenario", value_name="performance")
plt.figure(figsize=(11,7))
for name in long["option_name"].unique():
    subset = long[long["option_name"] == name]
    plt.plot(subset["scenario"], subset["performance"], marker="o", label=name)
plt.title("Strategic Options Across Scenarios"); plt.ylabel("Performance"); plt.xticks(rotation=25); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig(FIGURES / "options_across_scenarios.png", dpi=160); plt.close()

steps = np.arange(1, 41)
viability = pd.DataFrame({"time": steps})
for _, row in options.iterrows():
    state = np.zeros(len(steps)); cap = np.zeros(len(steps)); state[0] = 1.0; cap[0] = row["flexibility"]
    for t in range(1, len(steps)):
        if t < 18:
            shock = 0.03
            gain = 0.16*row["initial_return"] + 0.05*row["scalability"] - 0.04*row["carrying_cost"]
        else:
            shock = 0.15
            gain = 0.10*row["learning_value"] + 0.08*row["governance_readiness"] + 0.14*row["flexibility"] + 0.10*row["reversibility"] + 0.06*cap[t-1] - 0.16*row["lock_in_exposure"]
        cap[t] = np.clip(cap[t-1]+0.04*row["learning_value"]+0.04*row["governance_readiness"]+0.03*((row["flexibility"]+row["reversibility"]+row["modularity"])/3)-0.05*row["lock_in_exposure"]-0.03*row["carrying_cost"],0,1.2)
        state[t] = np.clip(state[t-1]+gain/4-shock/5,0,1.8)
    viability[row["option_name"]] = state
plt.figure(figsize=(11,7))
for col in viability.columns[1:]:
    plt.plot(viability["time"], viability[col], label=col)
plt.xlabel("Time Step"); plt.ylabel("Strategic Viability"); plt.title("Option Value and Strategic Flexibility Simulation"); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig(FIGURES / "option_value_simulation.png", dpi=160); plt.close()
options.to_csv(TABLES / "advanced_option_value_scores.csv", index=False)
viability.to_csv(TABLES / "option_value_simulation.csv", index=False)
print("Advanced option value analytics complete.")
