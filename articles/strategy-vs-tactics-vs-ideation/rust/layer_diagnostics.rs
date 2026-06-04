// Command-line layer diagnostics scaffold.
// Compile: rustc layer_diagnostics.rs -o layer_diagnostics
// Run: ./layer_diagnostics

#[derive(Debug)]
struct LayerProfile {
    name: &'static str,
    ideation: f64,
    strategy: f64,
    tactics: f64,
    feedback: f64,
    learning: f64,
}

fn alignment_score(p: &LayerProfile) -> f64 {
    0.18 * p.ideation + 0.24 * p.strategy + 0.22 * p.tactics + 0.18 * p.feedback + 0.18 * p.learning
}

fn diagnosis(p: &LayerProfile) -> &'static str {
    if p.tactics >= 0.65 && p.strategy < 0.55 {
        "tactical_overload"
    } else if p.ideation >= 0.75 && p.strategy < 0.55 {
        "selection_gap"
    } else if p.strategy >= 0.70 && p.tactics < 0.55 {
        "translation_gap"
    } else if p.feedback < 0.55 || p.learning < 0.55 {
        "learning_gap"
    } else {
        "monitor"
    }
}

fn main() {
    let profiles = vec![
        LayerProfile { name: "Tactically Busy", ideation: 0.32, strategy: 0.28, tactics: 0.39, feedback: 0.31, learning: 0.27 },
        LayerProfile { name: "Balanced Layered", ideation: 0.74, strategy: 0.79, tactics: 0.77, feedback: 0.75, learning: 0.76 },
        LayerProfile { name: "Ideation Heavy", ideation: 0.89, strategy: 0.41, tactics: 0.34, feedback: 0.42, learning: 0.46 },
    ];

    for profile in profiles {
        println!(
            "{} | score {:.3} | {}",
            profile.name,
            alignment_score(&profile),
            diagnosis(&profile)
        );
    }
}
