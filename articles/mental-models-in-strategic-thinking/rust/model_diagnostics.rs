// Command-line mental-model diagnostics scaffold.
// Compile: rustc model_diagnostics.rs -o model_diagnostics
// Run: ./model_diagnostics

#[derive(Debug)]
struct MentalModel {
    id: &'static str,
    systems: f64,
    probability: f64,
    flexibility: f64,
    plurality: f64,
    revision: f64,
    embedding: f64,
    ethics: f64,
    stakeholder: f64,
    evidence: f64,
}

fn adaptive_score(m: &MentalModel) -> f64 {
    0.17 * m.systems
        + 0.13 * m.probability
        + 0.16 * m.flexibility
        + 0.14 * m.plurality
        + 0.16 * m.revision
        - 0.08 * m.embedding
        + 0.12 * m.ethics
        + 0.10 * m.stakeholder
        + 0.10 * m.evidence
}

fn monoculture_risk(m: &MentalModel) -> f64 {
    0.28 * m.embedding
        + 0.20 * (1.0 - m.plurality)
        + 0.18 * (1.0 - m.flexibility)
        + 0.18 * (1.0 - m.revision)
        + 0.16 * (1.0 - m.stakeholder)
}

fn diagnosis(m: &MentalModel) -> &'static str {
    if adaptive_score(m) >= 0.75 && monoculture_risk(m) < 0.35 {
        "adaptive_model_strength"
    } else if monoculture_risk(m) >= 0.65 {
        "model_monoculture_or_lock_in_risk"
    } else if m.ethics < 0.45 || m.stakeholder < 0.45 {
        "ethical_or_stakeholder_blind_spot"
    } else {
        "requires_model_review"
    }
}

fn main() {
    let models = vec![
        MentalModel { id: "M001", systems: 0.24, probability: 0.21, flexibility: 0.19, plurality: 0.22, revision: 0.22, embedding: 0.58, ethics: 0.31, stakeholder: 0.28, evidence: 0.34 },
        MentalModel { id: "M003", systems: 0.89, probability: 0.84, flexibility: 0.88, plurality: 0.86, revision: 0.87, embedding: 0.71, ethics: 0.82, stakeholder: 0.80, evidence: 0.86 },
        MentalModel { id: "M004", systems: 0.33, probability: 0.29, flexibility: 0.18, plurality: 0.24, revision: 0.16, embedding: 0.91, ethics: 0.42, stakeholder: 0.39, evidence: 0.27 },
    ];

    for model in models {
        println!(
            "{} | adaptive {:.3} | risk {:.3} | {}",
            model.id,
            adaptive_score(&model),
            monoculture_risk(&model),
            diagnosis(&model)
        );
    }
}
