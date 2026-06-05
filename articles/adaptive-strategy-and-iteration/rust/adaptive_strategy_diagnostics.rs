// Command-line adaptive strategy diagnostics scaffold.
// Compile: rustc adaptive_strategy_diagnostics.rs -o adaptive_strategy_diagnostics
// Run: ./adaptive_strategy_diagnostics

#[derive(Debug)]
struct Strategy {
    id: &'static str,
    flexibility: f64,
    learning_capacity: f64,
    exploration: f64,
    exploitation_balance: f64,
    coherence: f64,
    feedback_intelligence: f64,
    governance: f64,
    systems_awareness: f64,
    learning_memory: f64,
}

fn adaptive_score(s: &Strategy) -> f64 {
    0.13 * s.flexibility
        + 0.15 * s.learning_capacity
        + 0.09 * s.exploration
        + 0.11 * s.exploitation_balance
        + 0.15 * s.coherence
        + 0.13 * s.feedback_intelligence
        + 0.10 * s.governance
        + 0.08 * s.systems_awareness
        + 0.06 * s.learning_memory
}

fn over_adaptation_risk(s: &Strategy) -> f64 {
    0.20 * s.flexibility * (1.0 - s.coherence)
        + 0.18 * (1.0 - s.governance)
        + 0.16 * (1.0 - s.feedback_intelligence)
        + 0.14 * (1.0 - s.learning_capacity)
        + 0.12 * (1.0 - s.exploitation_balance)
        + 0.10 * (1.0 - s.learning_memory)
        + 0.10 * (1.0 - s.systems_awareness)
}

fn recommendation(s: &Strategy) -> &'static str {
    if adaptive_score(s) >= 0.74 {
        "strong_adaptive_strategy_system"
    } else if over_adaptation_risk(s) >= 0.60 {
        "high_over_adaptation_or_reactivity_risk"
    } else if s.coherence < 0.45 {
        "strategic_drift_risk"
    } else {
        "developing_adaptive_capability"
    }
}

fn main() {
    let strategies = vec![
        Strategy { id: "AS001", flexibility: 0.24, learning_capacity: 0.31, exploration: 0.18, exploitation_balance: 0.74, coherence: 0.81, feedback_intelligence: 0.34, governance: 0.62, systems_awareness: 0.38, learning_memory: 0.36 },
        Strategy { id: "AS002", flexibility: 0.82, learning_capacity: 0.84, exploration: 0.68, exploitation_balance: 0.79, coherence: 0.76, feedback_intelligence: 0.82, governance: 0.78, systems_awareness: 0.74, learning_memory: 0.76 },
        Strategy { id: "AS004", flexibility: 0.86, learning_capacity: 0.49, exploration: 0.57, exploitation_balance: 0.32, coherence: 0.28, feedback_intelligence: 0.42, governance: 0.24, systems_awareness: 0.36, learning_memory: 0.30 },
    ];

    for s in strategies {
        println!(
            "{} | adaptive score {:.3} | over-adaptation risk {:.3} | {}",
            s.id,
            adaptive_score(&s),
            over_adaptation_risk(&s),
            recommendation(&s)
        );
    }
}
