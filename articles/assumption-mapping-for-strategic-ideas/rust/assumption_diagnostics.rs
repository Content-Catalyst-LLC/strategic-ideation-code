// Command-line assumption diagnostics scaffold.
// Compile: rustc assumption_diagnostics.rs -o assumption_diagnostics
// Run: ./assumption_diagnostics

#[derive(Debug)]
struct Assumption {
    id: &'static str,
    criticality: f64,
    uncertainty: f64,
    evidence_strength: f64,
    evidence_relevance: f64,
    evidence_transferability: f64,
    testability: f64,
    stakeholder_sensitivity: f64,
    system_sensitivity: f64,
}

fn evidence_composite(a: &Assumption) -> f64 {
    0.40 * a.evidence_strength + 0.30 * a.evidence_relevance + 0.30 * a.evidence_transferability
}

fn evidence_adjusted_risk(a: &Assumption) -> f64 {
    a.criticality * a.uncertainty * (1.0 - evidence_composite(a))
}

fn learning_value(a: &Assumption) -> f64 {
    0.34 * evidence_adjusted_risk(a)
        + 0.24 * a.testability
        + 0.18 * a.stakeholder_sensitivity
        + 0.14 * a.system_sensitivity
        + 0.10 * a.criticality
}

fn recommendation(a: &Assumption) -> &'static str {
    if evidence_adjusted_risk(a) >= 0.28 && a.testability >= 0.65 {
        "test_first"
    } else if evidence_adjusted_risk(a) >= 0.28 {
        "reduce_commitment_before_testing"
    } else if a.stakeholder_sensitivity >= 0.85 {
        "stakeholder_review_required"
    } else {
        "monitor"
    }
}

fn main() {
    let assumptions = vec![
        Assumption { id: "A001", criticality: 0.86, uncertainty: 0.70, evidence_strength: 0.38, evidence_relevance: 0.62, evidence_transferability: 0.54, testability: 0.78, stakeholder_sensitivity: 0.72, system_sensitivity: 0.70 },
        Assumption { id: "A004", criticality: 0.90, uncertainty: 0.72, evidence_strength: 0.34, evidence_relevance: 0.72, evidence_transferability: 0.60, testability: 0.74, stakeholder_sensitivity: 0.94, system_sensitivity: 0.76 },
        Assumption { id: "A015", criticality: 0.86, uncertainty: 0.66, evidence_strength: 0.38, evidence_relevance: 0.62, evidence_transferability: 0.52, testability: 0.62, stakeholder_sensitivity: 0.70, system_sensitivity: 0.74 },
    ];

    for a in assumptions {
        println!(
            "{} | risk {:.3} | learning {:.3} | {}",
            a.id,
            evidence_adjusted_risk(&a),
            learning_value(&a),
            recommendation(&a)
        );
    }
}
