// Command-line decision-making under uncertainty scoring scaffold.
// Compile: rustc decision_uncertainty_score.rs -o decision_uncertainty_score
// Run: ./decision_uncertainty_score

#[derive(Debug)]
struct OptionProfile {
    name: &'static str,
    expected_return: f64,
    robustness: f64,
    flexibility: f64,
    information_quality: f64,
    exposure: f64,
    option_value: f64,
    reversibility: f64,
    ethical_resilience: f64,
    learning_value: f64,
}

fn decision_profile(o: &OptionProfile) -> f64 {
    0.14 * o.expected_return
        + 0.18 * o.robustness
        + 0.16 * o.flexibility
        + 0.12 * o.information_quality
        - 0.16 * o.exposure
        + 0.14 * o.option_value
        + 0.10 * o.reversibility
        + 0.10 * o.ethical_resilience
        + 0.10 * o.learning_value
}

fn fragility_risk(o: &OptionProfile) -> f64 {
    0.24 * o.exposure
        + 0.18 * (1.0 - o.robustness)
        + 0.14 * (1.0 - o.flexibility)
        + 0.13 * (1.0 - o.option_value)
        + 0.12 * (1.0 - o.reversibility)
        + 0.10 * (1.0 - o.ethical_resilience)
        + 0.09 * (1.0 - o.information_quality)
}

fn main() {
    let options = vec![
        OptionProfile { name: "High-Return Brittle Option", expected_return: 0.86, robustness: 0.28, flexibility: 0.31, information_quality: 0.63, exposure: 0.82, option_value: 0.26, reversibility: 0.22, ethical_resilience: 0.38, learning_value: 0.30 },
        OptionProfile { name: "Balanced Robust Option", expected_return: 0.72, robustness: 0.79, flexibility: 0.74, information_quality: 0.72, exposure: 0.44, option_value: 0.72, reversibility: 0.68, ethical_resilience: 0.68, learning_value: 0.70 },
        OptionProfile { name: "Exploratory Optionality Option", expected_return: 0.61, robustness: 0.71, flexibility: 0.88, information_quality: 0.49, exposure: 0.53, option_value: 0.86, reversibility: 0.82, ethical_resilience: 0.62, learning_value: 0.88 },
    ];

    for o in options {
        println!(
            "{} | profile {:.3} | fragility {:.3}",
            o.name,
            decision_profile(&o),
            fragility_risk(&o)
        );
    }
}
