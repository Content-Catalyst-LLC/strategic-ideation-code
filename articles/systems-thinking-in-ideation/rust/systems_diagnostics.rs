// Command-line systems-ideation diagnostics scaffold.
// Compile: rustc systems_diagnostics.rs -o systems_diagnostics
// Run: ./systems_diagnostics

#[derive(Debug)]
struct SystemProfile {
    id: &'static str,
    feedback: f64,
    leverage: f64,
    root_cause: f64,
    stakeholder: f64,
    boundary: f64,
    stock_flow: f64,
    delay: f64,
    learning: f64,
    consequence_risk: f64,
    local_risk: f64,
}

fn score(s: &SystemProfile) -> f64 {
    0.14 * s.feedback
        + 0.14 * s.leverage
        + 0.13 * s.root_cause
        + 0.12 * s.stakeholder
        + 0.12 * s.boundary
        + 0.10 * s.stock_flow
        + 0.10 * s.delay
        + 0.13 * s.learning
        - 0.10 * s.consequence_risk
        - 0.08 * s.local_risk
}

fn symptom_focus_risk(s: &SystemProfile) -> f64 {
    (1.0 - s.root_cause) * 0.30
        + (1.0 - s.leverage) * 0.25
        + s.local_risk * 0.25
        + s.consequence_risk * 0.20
}

fn recommendation(s: &SystemProfile) -> &'static str {
    if score(s) >= 0.68 {
        "strong_systems_ideation_capacity"
    } else if symptom_focus_risk(s) >= 0.62 {
        "symptom_or_local_optimization_risk"
    } else if s.boundary < 0.50 {
        "boundary_review_required"
    } else {
        "develop_with_structural_review"
    }
}

fn main() {
    let systems = vec![
        SystemProfile { id: "SYS001", feedback: 0.24, leverage: 0.21, root_cause: 0.31, stakeholder: 0.28, boundary: 0.34, stock_flow: 0.30, delay: 0.26, learning: 0.29, consequence_risk: 0.79, local_risk: 0.76 },
        SystemProfile { id: "SYS003", feedback: 0.86, leverage: 0.91, root_cause: 0.88, stakeholder: 0.70, boundary: 0.78, stock_flow: 0.82, delay: 0.76, learning: 0.83, consequence_risk: 0.36, local_risk: 0.32 },
        SystemProfile { id: "SYS005", feedback: 0.78, leverage: 0.76, root_cause: 0.80, stakeholder: 0.90, boundary: 0.86, stock_flow: 0.74, delay: 0.72, learning: 0.82, consequence_risk: 0.34, local_risk: 0.30 },
    ];

    for system in systems {
        println!(
            "{} | score {:.3} | symptom risk {:.3} | {}",
            system.id,
            score(&system),
            symptom_focus_risk(&system),
            recommendation(&system)
        );
    }
}
