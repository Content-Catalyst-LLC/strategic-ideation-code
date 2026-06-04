// Command-line problem-framing diagnostics scaffold.
// Compile: rustc framing_diagnostics.rs -o framing_diagnostics
// Run: ./framing_diagnostics

#[derive(Debug)]
struct Frame {
    id: &'static str,
    boundary: f64,
    stakeholder: f64,
    systems: f64,
    causal: f64,
    assumptions: f64,
    reframing: f64,
    actionability: f64,
    lock_in: f64,
    politics: f64,
}

fn score(f: &Frame) -> f64 {
    0.16 * f.boundary
        + 0.15 * f.stakeholder
        + 0.15 * f.systems
        + 0.16 * f.causal
        + 0.12 * f.assumptions
        + 0.13 * f.reframing
        + 0.11 * f.actionability
        - 0.10 * f.lock_in
        - 0.08 * f.politics
}

fn symptom_framing_risk(f: &Frame) -> f64 {
    let boundary_gap = (0.70 - f.boundary).max(0.0);
    (1.0 - f.causal) * 0.30
        + (1.0 - f.systems) * 0.25
        + boundary_gap * 0.20
        + f.lock_in * 0.15
        + f.politics * 0.10
}

fn recommendation(f: &Frame) -> &'static str {
    if score(f) >= 0.68 {
        "strong_problem_framing_capacity"
    } else if symptom_framing_risk(f) >= 0.62 {
        "symptom_or_convenience_frame_risk"
    } else if f.boundary < 0.45 {
        "boundary_review_required"
    } else {
        "develop_with_frame_comparison"
    }
}

fn main() {
    let frames = vec![
        Frame { id: "F001", boundary: 0.28, stakeholder: 0.34, systems: 0.26, causal: 0.31, assumptions: 0.24, reframing: 0.22, actionability: 0.62, lock_in: 0.82, politics: 0.70 },
        Frame { id: "F003", boundary: 0.86, stakeholder: 0.79, systems: 0.91, causal: 0.84, assumptions: 0.78, reframing: 0.82, actionability: 0.72, lock_in: 0.32, politics: 0.34 },
        Frame { id: "F005", boundary: 0.82, stakeholder: 0.92, systems: 0.78, causal: 0.74, assumptions: 0.76, reframing: 0.80, actionability: 0.74, lock_in: 0.34, politics: 0.30 },
    ];

    for frame in frames {
        println!(
            "{} | score {:.3} | symptom risk {:.3} | {}",
            frame.id,
            score(&frame),
            symptom_framing_risk(&frame),
            recommendation(&frame)
        );
    }
}
