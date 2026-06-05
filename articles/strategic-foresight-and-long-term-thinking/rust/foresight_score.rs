// Command-line strategic foresight scoring scaffold.
// Compile: rustc foresight_score.rs -o foresight_score
// Run: ./foresight_score

#[derive(Debug)]
struct Strategy {
    name: &'static str,
    short_term_return: f64,
    foresight_depth: f64,
    resilience: f64,
    flexibility: f64,
    path_dependence_risk: f64,
    signal_capacity: f64,
    scenario_capacity: f64,
    option_value: f64,
    ethics_review: f64,
    governance_capacity: f64,
}

fn future_viability(s: &Strategy) -> f64 {
    0.18 * s.foresight_depth
        + 0.18 * s.resilience
        + 0.16 * s.flexibility
        + 0.14 * s.option_value
        + 0.12 * s.scenario_capacity
        + 0.10 * s.signal_capacity
        + 0.08 * s.governance_capacity
        + 0.08 * s.ethics_review
        - 0.14 * s.path_dependence_risk
}

fn short_term_bias(s: &Strategy) -> f64 {
    s.short_term_return - ((s.foresight_depth + s.resilience + s.flexibility + s.option_value) / 4.0)
}

fn recommendation(s: &Strategy) -> &'static str {
    if future_viability(s) >= 0.70 {
        "strong_long_term_foresight_profile"
    } else if short_term_bias(s) >= 0.35 {
        "short_term_optimization_risk"
    } else if s.path_dependence_risk >= 0.72 {
        "high_path_dependence_and_lock_in_risk"
    } else {
        "developing_foresight_capability"
    }
}

fn main() {
    let strategies = vec![
        Strategy { name: "Short-Term Efficiency Strategy", short_term_return: 0.86, foresight_depth: 0.24, resilience: 0.32, flexibility: 0.28, path_dependence_risk: 0.71, signal_capacity: 0.30, scenario_capacity: 0.26, option_value: 0.30, ethics_review: 0.34, governance_capacity: 0.42 },
        Strategy { name: "Balanced Foresight Strategy", short_term_return: 0.72, foresight_depth: 0.79, resilience: 0.76, flexibility: 0.74, path_dependence_risk: 0.39, signal_capacity: 0.76, scenario_capacity: 0.74, option_value: 0.72, ethics_review: 0.68, governance_capacity: 0.74 },
        Strategy { name: "Resilience-Biased Long-Horizon Strategy", short_term_return: 0.61, foresight_depth: 0.84, resilience: 0.88, flexibility: 0.79, path_dependence_risk: 0.34, signal_capacity: 0.80, scenario_capacity: 0.82, option_value: 0.78, ethics_review: 0.76, governance_capacity: 0.80 },
    ];

    for s in strategies {
        println!(
            "{} | future viability {:.3} | short-term bias {:.3} | {}",
            s.name,
            future_viability(&s),
            short_term_bias(&s),
            recommendation(&s)
        );
    }
}
