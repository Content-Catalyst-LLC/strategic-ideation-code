// Command-line game theory and strategic interaction scoring scaffold.
// Compile: rustc game_theory_score.rs -o game_theory_score
// Run: ./game_theory_score

#[derive(Debug)]
struct Setting {
    name: &'static str,
    rivalry: f64,
    coordination: f64,
    information_asymmetry: f64,
    retaliation: f64,
    institutional_support: f64,
    behavioral_realism: f64,
    mechanism_design: f64,
    ethical_complexity: f64,
}

fn mechanism_opportunity(s: &Setting) -> f64 {
    0.30 * s.mechanism_design
        + 0.18 * s.coordination
        + 0.16 * s.information_asymmetry
        + 0.14 * s.ethical_complexity
        + 0.12 * s.institutional_support
        + 0.10 * s.behavioral_realism
}

fn cooperation_fragility(s: &Setting) -> f64 {
    0.22 * s.rivalry
        + 0.20 * s.retaliation
        + 0.16 * s.information_asymmetry
        + 0.12 * s.ethical_complexity
        - 0.15 * s.institutional_support
        - 0.15 * s.coordination
}

fn main() {
    let settings = vec![
        Setting { name: "Price Competition Environment", rivalry: 0.84, coordination: 0.28, information_asymmetry: 0.44, retaliation: 0.76, institutional_support: 0.39, behavioral_realism: 0.52, mechanism_design: 0.42, ethical_complexity: 0.46 },
        Setting { name: "Standards Coordination Environment", rivalry: 0.36, coordination: 0.86, information_asymmetry: 0.31, retaliation: 0.24, institutional_support: 0.73, behavioral_realism: 0.68, mechanism_design: 0.78, ethical_complexity: 0.54 },
        Setting { name: "Platform Ecosystem Environment", rivalry: 0.71, coordination: 0.74, information_asymmetry: 0.69, retaliation: 0.58, institutional_support: 0.57, behavioral_realism: 0.74, mechanism_design: 0.82, ethical_complexity: 0.76 },
    ];

    for s in settings {
        println!(
            "{} | mechanism opportunity {:.3} | cooperation fragility {:.3}",
            s.name,
            mechanism_opportunity(&s),
            cooperation_fragility(&s)
        );
    }
}
