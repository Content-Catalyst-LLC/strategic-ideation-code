// Command-line conceptual clarity diagnostics scaffold.
// Compile: rustc conceptual_clarity_diagnostics.rs -o conceptual_clarity_diagnostics
// Run: ./conceptual_clarity_diagnostics

#[derive(Debug)]
struct Concept {
    id: &'static str,
    definition: f64,
    boundary: f64,
    distinction: f64,
    operational: f64,
    measurement: f64,
    revision: f64,
    stakeholder: f64,
    ethics: f64,
    governance: f64,
}

fn clarity_score(c: &Concept) -> f64 {
    0.17 * c.definition
        + 0.14 * c.boundary
        + 0.14 * c.distinction
        + 0.13 * c.operational
        + 0.15 * c.measurement
        + 0.10 * c.revision
        + 0.07 * c.stakeholder
        + 0.06 * c.ethics
        + 0.04 * c.governance
}

fn diagnosis(c: &Concept) -> &'static str {
    if c.definition < 0.45 && c.measurement < 0.45 {
        "high_false_precision_risk"
    } else if c.boundary < 0.40 {
        "concept_expansion_or_boundary_risk"
    } else if c.revision < 0.35 {
        "conceptual_drift_risk"
    } else if clarity_score(c) >= 0.64 {
        "usable_for_strategy"
    } else {
        "requires_clarity_review"
    }
}

fn main() {
    let concepts = vec![
        Concept { id: "CC001", definition: 0.42, boundary: 0.31, distinction: 0.44, operational: 0.52, measurement: 0.36, revision: 0.29, stakeholder: 0.46, ethics: 0.41, governance: 0.30 },
        Concept { id: "CC003", definition: 0.64, boundary: 0.55, distinction: 0.68, operational: 0.70, measurement: 0.60, revision: 0.52, stakeholder: 0.66, ethics: 0.71, governance: 0.50 },
        Concept { id: "CC005", definition: 0.35, boundary: 0.28, distinction: 0.33, operational: 0.40, measurement: 0.30, revision: 0.27, stakeholder: 0.43, ethics: 0.39, governance: 0.25 },
    ];

    for concept in concepts {
        println!("{} | {:.3} | {}", concept.id, clarity_score(&concept), diagnosis(&concept));
    }
}
