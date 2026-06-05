// Command-line strategic tradeoff scoring scaffold.
// Compile: rustc risk_tradeoff_score.rs -o risk_tradeoff_score
// Run: ./risk_tradeoff_score

#[derive(Debug)]
struct OptionProfile {
    name: &'static str,
    short_term_return: f64,
    resilience: f64,
    flexibility: f64,
    legitimacy: f64,
    opportunity_value: f64,
    exposure: f64,
    reversibility: f64,
    ethical_resilience: f64,
    learning_value: f64,
}

fn tradeoff_score(o: &OptionProfile) -> f64 {
    0.18 * o.short_term_return
        + 0.20 * o.resilience
        + 0.16 * o.flexibility
        + 0.14 * o.legitimacy
        + 0.14 * o.opportunity_value
        - 0.18 * o.exposure
        + 0.08 * o.reversibility
        + 0.08 * o.ethical_resilience
        + 0.08 * o.learning_value
}

fn fragility_warning(o: &OptionProfile) -> f64 {
    0.26 * o.exposure
        + 0.18 * (1.0 - o.resilience)
        + 0.14 * (1.0 - o.flexibility)
        + 0.12 * (1.0 - o.legitimacy)
        + 0.12 * (1.0 - o.opportunity_value)
        + 0.10 * (1.0 - o.reversibility)
        + 0.08 * (1.0 - o.ethical_resilience)
}

fn main() {
    let options = vec![
        OptionProfile { name: "Efficiency-Optimized Option", short_term_return: 0.86, resilience: 0.32, flexibility: 0.36, legitimacy: 0.48, opportunity_value: 0.34, exposure: 0.74, reversibility: 0.30, ethical_resilience: 0.42, learning_value: 0.34 },
        OptionProfile { name: "Balanced Strategic Option", short_term_return: 0.71, resilience: 0.74, flexibility: 0.76, legitimacy: 0.72, opportunity_value: 0.70, exposure: 0.46, reversibility: 0.68, ethical_resilience: 0.70, learning_value: 0.72 },
        OptionProfile { name: "Resilience-First Option", short_term_return: 0.58, resilience: 0.88, flexibility: 0.79, legitimacy: 0.81, opportunity_value: 0.76, exposure: 0.34, reversibility: 0.72, ethical_resilience: 0.82, learning_value: 0.70 },
    ];

    for option in options {
        println!(
            "{} | tradeoff score {:.3} | fragility warning {:.3}",
            option.name,
            tradeoff_score(&option),
            fragility_warning(&option)
        );
    }
}
