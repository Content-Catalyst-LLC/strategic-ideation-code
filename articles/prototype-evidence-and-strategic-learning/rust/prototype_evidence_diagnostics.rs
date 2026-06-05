// Command-line prototype evidence diagnostics scaffold.
// Compile: rustc prototype_evidence_diagnostics.rs -o prototype_evidence_diagnostics
// Run: ./prototype_evidence_diagnostics

#[derive(Debug)]
struct PrototypeSystem {
    id: &'static str,
    assumption_clarity: f64,
    learning_target_fit: f64,
    evidence_quality: f64,
    behavioral_grounding: f64,
    context_realism: f64,
    systems_awareness: f64,
    decision_linkage: f64,
    ethical_review: f64,
    learning_memory: f64,
}

fn learning_quality(s: &PrototypeSystem) -> f64 {
    0.13 * s.assumption_clarity
        + 0.13 * s.learning_target_fit
        + 0.15 * s.evidence_quality
        + 0.13 * s.behavioral_grounding
        + 0.11 * s.context_realism
        + 0.11 * s.systems_awareness
        + 0.11 * s.decision_linkage
        + 0.07 * s.ethical_review
        + 0.06 * s.learning_memory
}

fn validation_theater_risk(s: &PrototypeSystem) -> f64 {
    0.17 * (1.0 - s.assumption_clarity)
        + 0.16 * (1.0 - s.evidence_quality)
        + 0.14 * (1.0 - s.behavioral_grounding)
        + 0.13 * (1.0 - s.decision_linkage)
        + 0.12 * (1.0 - s.learning_memory)
        + 0.11 * (1.0 - s.systems_awareness)
        + 0.09 * (1.0 - s.ethical_review)
        + 0.08 * (1.0 - s.context_realism)
}

fn recommendation(s: &PrototypeSystem) -> &'static str {
    if learning_quality(s) >= 0.72 {
        "strong_prototype_learning_system"
    } else if validation_theater_risk(s) >= 0.68 {
        "high_validation_theater_risk"
    } else if s.behavioral_grounding < 0.36 {
        "evidence_lacks_behavioral_grounding"
    } else {
        "developing_prototype_learning_capability"
    }
}

fn main() {
    let systems = vec![
        PrototypeSystem { id: "PE001", assumption_clarity: 0.30, learning_target_fit: 0.28, evidence_quality: 0.26, behavioral_grounding: 0.22, context_realism: 0.34, systems_awareness: 0.24, decision_linkage: 0.20, ethical_review: 0.28, learning_memory: 0.22 },
        PrototypeSystem { id: "PE004", assumption_clarity: 0.84, learning_target_fit: 0.82, evidence_quality: 0.84, behavioral_grounding: 0.76, context_realism: 0.80, systems_awareness: 0.88, decision_linkage: 0.82, ethical_review: 0.72, learning_memory: 0.82 },
        PrototypeSystem { id: "PE007", assumption_clarity: 0.52, learning_target_fit: 0.46, evidence_quality: 0.40, behavioral_grounding: 0.26, context_realism: 0.32, systems_awareness: 0.30, decision_linkage: 0.38, ethical_review: 0.36, learning_memory: 0.34 },
    ];

    for s in systems {
        println!(
            "{} | learning quality {:.3} | validation theater risk {:.3} | {}",
            s.id,
            learning_quality(&s),
            validation_theater_risk(&s),
            recommendation(&s)
        );
    }
}
