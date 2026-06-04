// Command-line strategic hypothesis diagnostics scaffold.
// Compile: rustc hypothesis_diagnostics.rs -o hypothesis_diagnostics
// Run: ./hypothesis_diagnostics

#[derive(Debug)]
struct Hypothesis {
    id: &'static str,
    explanatory: f64,
    testability: f64,
    evidence: f64,
    relevance: f64,
    stakeholder: f64,
    systems: f64,
    actionability: f64,
    risk: f64,
    reversibility: f64,
}

fn score(h: &Hypothesis) -> f64 {
    0.16 * h.explanatory
        + 0.14 * h.testability
        + 0.14 * h.evidence
        + 0.16 * h.relevance
        + 0.12 * h.stakeholder
        + 0.12 * h.systems
        + 0.10 * h.actionability
        + 0.06 * h.reversibility
        - 0.10 * h.risk
}

fn recommendation(h: &Hypothesis) -> &'static str {
    let value = score(h);
    if value >= 0.72 && h.evidence >= 0.65 && h.reversibility >= 0.55 {
        "prototype_or_pilot"
    } else if value >= 0.64 {
        "targeted_research_or_low_risk_test"
    } else if value >= 0.54 {
        "monitor_and_compare"
    } else {
        "hold_reframe_or_archive"
    }
}

fn main() {
    let hypotheses = vec![
        Hypothesis { id: "H001", explanatory: 0.82, testability: 0.74, evidence: 0.68, relevance: 0.86, stakeholder: 0.72, systems: 0.76, actionability: 0.72, risk: 0.52, reversibility: 0.74 },
        Hypothesis { id: "H004", explanatory: 0.84, testability: 0.70, evidence: 0.66, relevance: 0.86, stakeholder: 0.92, systems: 0.78, actionability: 0.64, risk: 0.58, reversibility: 0.66 },
        Hypothesis { id: "H010", explanatory: 0.88, testability: 0.68, evidence: 0.72, relevance: 0.90, stakeholder: 0.66, systems: 0.86, actionability: 0.62, risk: 0.66, reversibility: 0.58 },
    ];

    for hypothesis in hypotheses {
        println!(
            "{} | score {:.3} | {}",
            hypothesis.id,
            score(&hypothesis),
            recommendation(&hypothesis)
        );
    }
}
