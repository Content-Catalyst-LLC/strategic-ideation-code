// Command-line co-design diagnostics scaffold.
// Compile: rustc codesign_diagnostics.rs -o codesign_diagnostics
// Run: ./codesign_diagnostics

#[derive(Debug)]
struct ParticipationSystem {
    id: &'static str,
    representation: f64,
    influence: f64,
    accessibility: f64,
    reciprocity: f64,
    power_awareness: f64,
    knowledge_integration: f64,
    decision_linkage: f64,
    accountability: f64,
    learning_memory: f64,
}

fn participation_quality(s: &ParticipationSystem) -> f64 {
    0.13 * s.representation
        + 0.15 * s.influence
        + 0.11 * s.accessibility
        + 0.11 * s.reciprocity
        + 0.13 * s.power_awareness
        + 0.12 * s.knowledge_integration
        + 0.11 * s.decision_linkage
        + 0.10 * s.accountability
        + 0.04 * s.learning_memory
}

fn tokenism_risk(s: &ParticipationSystem) -> f64 {
    0.16 * (1.0 - s.influence)
        + 0.14 * (1.0 - s.decision_linkage)
        + 0.14 * (1.0 - s.accountability)
        + 0.13 * (1.0 - s.reciprocity)
        + 0.13 * (1.0 - s.power_awareness)
        + 0.11 * (1.0 - s.representation)
        + 0.10 * (1.0 - s.accessibility)
        + 0.09 * (1.0 - s.learning_memory)
}

fn recommendation(s: &ParticipationSystem) -> &'static str {
    if participation_quality(s) >= 0.72 {
        "strong_participatory_codesign_system"
    } else if tokenism_risk(s) >= 0.68 {
        "high_tokenism_or_extractive_participation_risk"
    } else if s.influence < 0.36 {
        "participation_has_low_decision_influence"
    } else {
        "developing_participatory_capability"
    }
}

fn main() {
    let systems = vec![
        ParticipationSystem { id: "P001", representation: 0.34, influence: 0.22, accessibility: 0.40, reciprocity: 0.24, power_awareness: 0.28, knowledge_integration: 0.42, decision_linkage: 0.20, accountability: 0.18, learning_memory: 0.24 },
        ParticipationSystem { id: "P004", representation: 0.86, influence: 0.84, accessibility: 0.82, reciprocity: 0.80, power_awareness: 0.86, knowledge_integration: 0.84, decision_linkage: 0.82, accountability: 0.86, learning_memory: 0.84 },
        ParticipationSystem { id: "P008", representation: 0.58, influence: 0.24, accessibility: 0.52, reciprocity: 0.18, power_awareness: 0.30, knowledge_integration: 0.54, decision_linkage: 0.22, accountability: 0.16, learning_memory: 0.20 },
    ];

    for s in systems {
        println!(
            "{} | participation quality {:.3} | tokenism risk {:.3} | {}",
            s.id,
            participation_quality(&s),
            tokenism_risk(&s),
            recommendation(&s)
        );
    }
}
