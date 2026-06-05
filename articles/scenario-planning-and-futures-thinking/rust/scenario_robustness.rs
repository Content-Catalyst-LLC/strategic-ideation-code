// Command-line scenario robustness scaffold.
// Compile: rustc scenario_robustness.rs -o scenario_robustness
// Run: ./scenario_robustness

#[derive(Debug)]
struct Strategy {
    name: &'static str,
    scenario_values: [f64; 5],
    flexibility: f64,
    implementation_readiness: f64,
    ethical_resilience: f64,
    option_value: f64,
}

fn mean(values: &[f64]) -> f64 {
    values.iter().sum::<f64>() / values.len() as f64
}

fn stddev(values: &[f64]) -> f64 {
    let m = mean(values);
    let variance = values.iter().map(|v| (v - m).powi(2)).sum::<f64>() / values.len() as f64;
    variance.sqrt()
}

fn robustness_profile(s: &Strategy) -> f64 {
    let worst = s.scenario_values.iter().copied().fold(1.0, f64::min);
    let avg = mean(&s.scenario_values);
    let vol = stddev(&s.scenario_values);

    0.30 * worst
        + 0.24 * avg
        + 0.16 * s.flexibility
        + 0.12 * s.implementation_readiness
        + 0.10 * s.ethical_resilience
        + 0.10 * s.option_value
        - 0.12 * vol
}

fn main() {
    let strategies = vec![
        Strategy { name: "Short-Term Optimization Strategy", scenario_values: [0.84, 0.41, 0.36, 0.48, 0.38], flexibility: 0.28, implementation_readiness: 0.86, ethical_resilience: 0.42, option_value: 0.30 },
        Strategy { name: "Balanced Adaptive Strategy", scenario_values: [0.74, 0.71, 0.67, 0.70, 0.66], flexibility: 0.73, implementation_readiness: 0.74, ethical_resilience: 0.68, option_value: 0.72 },
        Strategy { name: "Resilience-Oriented Strategy", scenario_values: [0.68, 0.75, 0.79, 0.73, 0.76], flexibility: 0.82, implementation_readiness: 0.66, ethical_resilience: 0.76, option_value: 0.78 },
    ];

    for s in strategies {
        println!(
            "{} | mean {:.3} | worst {:.3} | robustness {:.3}",
            s.name,
            mean(&s.scenario_values),
            s.scenario_values.iter().copied().fold(1.0, f64::min),
            robustness_profile(&s)
        );
    }
}
