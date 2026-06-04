// Command-line lateral thinking diagnostics scaffold.
// Compile: rustc lateral_diagnostics.rs -o lateral_diagnostics
// Run: ./lateral_diagnostics

#[derive(Debug)]
struct Context {
    id: &'static str,
    frame_rigidity: f64,
    provocation: f64,
    analogical_distance: f64,
    random_entry: f64,
    reversal: f64,
    challenge: f64,
    convergence: f64,
    systems: f64,
    legitimacy: f64,
    political_safety: f64,
    transformation: f64,
}

fn lateral_profile(c: &Context) -> f64 {
    -0.14 * c.frame_rigidity
        + 0.14 * c.provocation
        + 0.12 * c.analogical_distance
        + 0.09 * c.random_entry
        + 0.10 * c.reversal
        + 0.10 * c.challenge
        + 0.14 * c.convergence
        + 0.12 * c.systems
        + 0.08 * c.legitimacy
        + 0.07 * c.political_safety
        + 0.14 * c.transformation
}

fn frame_rigidity_risk(c: &Context) -> f64 {
    c.frame_rigidity * (1.0 - c.provocation)
}

fn drift_risk(c: &Context) -> f64 {
    c.transformation * (1.0 - c.convergence)
}

fn diagnosis(c: &Context) -> &'static str {
    if frame_rigidity_risk(c) >= 0.55 {
        "frame_rigidity_risk"
    } else if drift_risk(c) >= 0.45 {
        "unintegrated_novelty_risk"
    } else if c.legitimacy < 0.50 {
        "stakeholder_legitimacy_gap"
    } else if lateral_profile(c) >= 0.50 {
        "strong_lateral_system"
    } else {
        "requires_lateral_process_review"
    }
}

fn main() {
    let contexts = vec![
        Context { id: "LT001", frame_rigidity: 0.86, provocation: 0.18, analogical_distance: 0.21, random_entry: 0.16, reversal: 0.20, challenge: 0.28, convergence: 0.72, systems: 0.44, legitimacy: 0.50, political_safety: 0.48, transformation: 0.24 },
        Context { id: "LT004", frame_rigidity: 0.36, provocation: 0.74, analogical_distance: 0.76, random_entry: 0.70, reversal: 0.78, challenge: 0.80, convergence: 0.82, systems: 0.86, legitimacy: 0.78, political_safety: 0.74, transformation: 0.88 },
        Context { id: "LT008", frame_rigidity: 0.52, provocation: 0.78, analogical_distance: 0.68, random_entry: 0.72, reversal: 0.70, challenge: 0.46, convergence: 0.28, systems: 0.34, legitimacy: 0.36, political_safety: 0.40, transformation: 0.62 },
    ];

    for context in contexts {
        println!(
            "{} | profile {:.3} | rigidity {:.3} | drift {:.3} | {}",
            context.id,
            lateral_profile(&context),
            frame_rigidity_risk(&context),
            drift_risk(&context),
            diagnosis(&context)
        );
    }
}
