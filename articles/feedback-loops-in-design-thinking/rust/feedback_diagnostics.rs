// Command-line feedback diagnostics scaffold.
// Compile: rustc feedback_diagnostics.rs -o feedback_diagnostics
// Run: ./feedback_diagnostics

#[derive(Debug)]
struct FeedbackSystem {
    id: &'static str,
    signal_quality: f64,
    interpretation_capacity: f64,
    adjustment_speed: f64,
    user_insight_depth: f64,
    stability: f64,
    ethical_integrity: f64,
    systems_awareness: f64,
    decision_linkage: f64,
    learning_memory: f64,
}

fn feedback_profile(s: &FeedbackSystem) -> f64 {
    0.13 * s.signal_quality
        + 0.13 * s.interpretation_capacity
        + 0.10 * s.adjustment_speed
        + 0.13 * s.user_insight_depth
        + 0.10 * s.stability
        + 0.11 * s.ethical_integrity
        + 0.10 * s.systems_awareness
        + 0.10 * s.decision_linkage
        + 0.10 * s.learning_memory
}

fn noisy_churn_risk(s: &FeedbackSystem) -> f64 {
    0.16 * s.adjustment_speed
        + 0.15 * (1.0 - s.signal_quality)
        + 0.15 * (1.0 - s.interpretation_capacity)
        + 0.13 * (1.0 - s.stability)
        + 0.12 * (1.0 - s.systems_awareness)
        + 0.12 * (1.0 - s.ethical_integrity)
        + 0.10 * (1.0 - s.decision_linkage)
        + 0.07 * (1.0 - s.learning_memory)
}

fn recommendation(s: &FeedbackSystem) -> &'static str {
    if feedback_profile(s) >= 0.68 {
        "strong_feedback_learning_system"
    } else if noisy_churn_risk(s) >= 0.64 {
        "high_noisy_churn_or_feedback_theater_risk"
    } else if s.decision_linkage < 0.40 {
        "feedback_not_linked_to_decisions"
    } else {
        "developing_feedback_capability"
    }
}

fn main() {
    let systems = vec![
        FeedbackSystem { id: "F001", signal_quality: 0.34, interpretation_capacity: 0.31, adjustment_speed: 0.29, user_insight_depth: 0.36, stability: 0.41, ethical_integrity: 0.38, systems_awareness: 0.32, decision_linkage: 0.28, learning_memory: 0.26 },
        FeedbackSystem { id: "F004", signal_quality: 0.82, interpretation_capacity: 0.84, adjustment_speed: 0.63, user_insight_depth: 0.88, stability: 0.72, ethical_integrity: 0.72, systems_awareness: 0.84, decision_linkage: 0.80, learning_memory: 0.82 },
        FeedbackSystem { id: "F006", signal_quality: 0.62, interpretation_capacity: 0.42, adjustment_speed: 0.34, user_insight_depth: 0.46, stability: 0.50, ethical_integrity: 0.40, systems_awareness: 0.38, decision_linkage: 0.24, learning_memory: 0.28 },
    ];

    for s in systems {
        println!(
            "{} | feedback profile {:.3} | noisy churn risk {:.3} | {}",
            s.id,
            feedback_profile(&s),
            noisy_churn_risk(&s),
            recommendation(&s)
        );
    }
}
