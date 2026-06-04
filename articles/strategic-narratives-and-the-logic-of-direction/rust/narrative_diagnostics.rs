// Command-line strategic narrative diagnostics scaffold.
// Compile: rustc narrative_diagnostics.rs -o narrative_diagnostics
// Run: ./narrative_diagnostics

#[derive(Debug)]
struct Narrative {
    id: &'static str,
    diagnosis: f64,
    purpose: f64,
    choice: f64,
    sequence: f64,
    role: f64,
    future: f64,
    accountability: f64,
    evidence: f64,
    stakeholder: f64,
    ethics: f64,
}

fn coherence_score(n: &Narrative) -> f64 {
    0.14 * n.diagnosis
        + 0.12 * n.purpose
        + 0.14 * n.choice
        + 0.12 * n.sequence
        + 0.11 * n.role
        + 0.10 * n.future
        + 0.11 * n.accountability
        + 0.08 * n.evidence
        + 0.05 * n.stakeholder
        + 0.03 * n.ethics
}

fn diagnosis(n: &Narrative) -> &'static str {
    if n.choice < 0.40 {
        "weak_choice_logic"
    } else if n.sequence < 0.40 {
        "weak_pathway_logic"
    } else if n.accountability < 0.40 {
        "narrative_performance_gap_risk"
    } else if coherence_score(n) >= 0.72 {
        "strong_directional_narrative"
    } else {
        "requires_narrative_review"
    }
}

fn main() {
    let narratives = vec![
        Narrative { id: "SN001", diagnosis: 0.32, purpose: 0.44, choice: 0.28, sequence: 0.30, role: 0.36, future: 0.42, accountability: 0.25, evidence: 0.34, stakeholder: 0.38, ethics: 0.35 },
        Narrative { id: "SN003", diagnosis: 0.86, purpose: 0.82, choice: 0.76, sequence: 0.84, role: 0.78, future: 0.80, accountability: 0.82, evidence: 0.84, stakeholder: 0.78, ethics: 0.81 },
        Narrative { id: "SN004", diagnosis: 0.41, purpose: 0.48, choice: 0.35, sequence: 0.33, role: 0.39, future: 0.45, accountability: 0.31, evidence: 0.40, stakeholder: 0.43, ethics: 0.39 },
    ];

    for narrative in narratives {
        println!("{} | {:.3} | {}", narrative.id, coherence_score(&narrative), diagnosis(&narrative));
    }
}
