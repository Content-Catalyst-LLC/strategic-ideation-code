// Command-line experimentation diagnostics scaffold.
// Compile: rustc experiment_diagnostics.rs -o experiment_diagnostics
// Run: ./experiment_diagnostics

#[derive(Debug)]
struct System {
    id: &'static str,
    speed: f64,
    cost_efficiency: f64,
    insight_depth: f64,
    user_validation: f64,
    assumption_criticality: f64,
    evidence_quality: f64,
    systems_awareness: f64,
    ethical_review: f64,
    decision_linkage: f64,
    learning_memory: f64,
}

fn experimentation_profile(s: &System) -> f64 {
    0.10 * s.speed
        + 0.09 * s.cost_efficiency
        + 0.15 * s.insight_depth
        + 0.12 * s.user_validation
        + 0.12 * s.assumption_criticality
        + 0.14 * s.evidence_quality
        + 0.10 * s.systems_awareness
        + 0.08 * s.ethical_review
        + 0.10 * s.decision_linkage
        + 0.10 * s.learning_memory
}

fn superficial_testing_risk(s: &System) -> f64 {
    0.14 * s.speed
        + 0.16 * (1.0 - s.insight_depth)
        + 0.15 * (1.0 - s.evidence_quality)
        + 0.13 * (1.0 - s.systems_awareness)
        + 0.13 * (1.0 - s.ethical_review)
        + 0.13 * (1.0 - s.decision_linkage)
        + 0.09 * (1.0 - s.assumption_criticality)
        + 0.07 * (1.0 - s.learning_memory)
}

fn recommendation(s: &System) -> &'static str {
    if experimentation_profile(s) >= 0.66 {
        "strong_experimentation_learning_system"
    } else if superficial_testing_risk(s) >= 0.62 {
        "high_superficial_testing_or_prototype_theater_risk"
    } else if s.decision_linkage < 0.42 {
        "learning_not_linked_to_decisions"
    } else {
        "developing_experimentation_capability"
    }
}

fn main() {
    let systems = vec![
        System { id: "E001", speed: 0.24, cost_efficiency: 0.31, insight_depth: 0.42, user_validation: 0.36, assumption_criticality: 0.44, evidence_quality: 0.38, systems_awareness: 0.34, ethical_review: 0.42, decision_linkage: 0.30, learning_memory: 0.32 },
        System { id: "E004", speed: 0.61, cost_efficiency: 0.67, insight_depth: 0.89, user_validation: 0.84, assumption_criticality: 0.86, evidence_quality: 0.88, systems_awareness: 0.82, ethical_review: 0.70, decision_linkage: 0.82, learning_memory: 0.80 },
        System { id: "E006", speed: 0.70, cost_efficiency: 0.50, insight_depth: 0.36, user_validation: 0.42, assumption_criticality: 0.38, evidence_quality: 0.34, systems_awareness: 0.28, ethical_review: 0.30, decision_linkage: 0.24, learning_memory: 0.22 },
    ];

    for s in systems {
        println!(
            "{} | experimentation profile {:.3} | superficial testing risk {:.3} | {}",
            s.id,
            experimentation_profile(&s),
            superficial_testing_risk(&s),
            recommendation(&s)
        );
    }
}
