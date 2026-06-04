// Command-line second-order effects diagnostics scaffold.
// Compile: rustc second_order_diagnostics.rs -o second_order_diagnostics
// Run: ./second_order_diagnostics

#[derive(Debug)]
struct Intervention {
    id: &'static str,
    first_gain: f64,
    adaptation: f64,
    feedback: f64,
    delay: f64,
    burden: f64,
    gaming: f64,
    fragility: f64,
    learning: f64,
    legitimacy: f64,
    reversibility: f64,
}

fn second_order_risk(i: &Intervention) -> f64 {
    0.16 * i.adaptation
        + 0.15 * i.feedback
        + 0.14 * i.delay
        + 0.15 * i.burden
        + 0.14 * i.gaming
        + 0.16 * i.fragility
        - 0.10 * i.learning
        - 0.06 * i.legitimacy
        - 0.06 * i.reversibility
}

fn false_success_risk(i: &Intervention) -> f64 {
    0.26 * i.first_gain
        + 0.20 * i.fragility
        + 0.16 * i.delay
        + 0.14 * i.gaming
        + 0.12 * i.burden
        - 0.16 * i.learning
}

fn recommendation(i: &Intervention) -> &'static str {
    if false_success_risk(i) >= 0.55 {
        "false_first_order_success_risk"
    } else if i.gaming >= 0.70 {
        "gaming_and_metric_distortion_risk"
    } else if i.burden >= 0.70 {
        "burden_shift_risk"
    } else if second_order_risk(i) >= 0.50 {
        "second_order_review_required"
    } else {
        "monitor_with_learning_loop"
    }
}

fn main() {
    let interventions = vec![
        Intervention { id: "I001", first_gain: 0.88, adaptation: 0.76, feedback: 0.58, delay: 0.69, burden: 0.66, gaming: 0.52, fragility: 0.82, learning: 0.38, legitimacy: 0.44, reversibility: 0.42 },
        Intervention { id: "I002", first_gain: 0.71, adaptation: 0.44, feedback: 0.51, delay: 0.42, burden: 0.34, gaming: 0.28, fragility: 0.39, learning: 0.76, legitimacy: 0.72, reversibility: 0.70 },
        Intervention { id: "I003", first_gain: 0.63, adaptation: 0.81, feedback: 0.73, delay: 0.57, burden: 0.78, gaming: 0.74, fragility: 0.74, learning: 0.42, legitimacy: 0.46, reversibility: 0.38 },
    ];

    for intervention in interventions {
        println!(
            "{} | second-order risk {:.3} | false-success risk {:.3} | {}",
            intervention.id,
            second_order_risk(&intervention),
            false_success_risk(&intervention),
            recommendation(&intervention)
        );
    }
}
