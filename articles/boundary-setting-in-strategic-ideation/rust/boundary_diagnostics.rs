// Command-line boundary diagnostics scaffold.
// Compile: rustc boundary_diagnostics.rs -o boundary_diagnostics
// Run: ./boundary_diagnostics

#[derive(Debug)]
struct Boundary {
    id: &'static str,
    problem: f64,
    system: f64,
    stakeholder: f64,
    causal: f64,
    temporal: f64,
    institutional: f64,
    evidence: f64,
    ethical: f64,
    revision: f64,
    actionability: f64,
}

fn boundary_quality(b: &Boundary) -> f64 {
    0.12 * b.problem
        + 0.13 * b.system
        + 0.14 * b.stakeholder
        + 0.14 * b.causal
        + 0.12 * b.temporal
        + 0.11 * b.institutional
        + 0.11 * b.evidence
        + 0.10 * b.ethical
        + 0.09 * b.revision
        + 0.04 * b.actionability
}

fn diagnosis(b: &Boundary) -> &'static str {
    let q = boundary_quality(b);
    if q >= 0.78 {
        "strong_boundary_design"
    } else if b.stakeholder < 0.40 {
        "stakeholder_exclusion_risk"
    } else if b.temporal < 0.40 {
        "temporal_boundary_risk"
    } else if b.causal < 0.45 {
        "causal_boundary_risk"
    } else {
        "usable_with_boundary_review"
    }
}

fn main() {
    let boundaries = vec![
        Boundary { id: "B001", problem: 0.62, system: 0.38, stakeholder: 0.34, causal: 0.42, temporal: 0.38, institutional: 0.50, evidence: 0.40, ethical: 0.32, revision: 0.38, actionability: 0.82 },
        Boundary { id: "B003", problem: 0.82, system: 0.90, stakeholder: 0.72, causal: 0.88, temporal: 0.76, institutional: 0.78, evidence: 0.74, ethical: 0.70, revision: 0.72, actionability: 0.58 },
        Boundary { id: "B005", problem: 0.84, system: 0.86, stakeholder: 0.82, causal: 0.82, temporal: 0.84, institutional: 0.80, evidence: 0.86, ethical: 0.84, revision: 0.90, actionability: 0.66 },
    ];

    for boundary in boundaries {
        println!(
            "{} | boundary quality {:.3} | {}",
            boundary.id,
            boundary_quality(&boundary),
            diagnosis(&boundary)
        );
    }
}
