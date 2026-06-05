// Command-line implementation profile scoring scaffold.
// Compile: rustc implementation_score.rs -o implementation_score
// Run: ./implementation_score

struct ImplementationProfile {
    name: &'static str,
    goal: f64,
    coordination: f64,
    structure: f64,
    culture: f64,
    incentives: f64,
    resources: f64,
    communication: f64,
    accountability: f64,
    adaptation: f64,
}

fn implementation_score(p: &ImplementationProfile) -> f64 {
    0.12 * p.goal
        + 0.15 * p.coordination
        + 0.12 * p.structure
        + 0.12 * p.culture
        + 0.13 * p.incentives
        + 0.12 * p.resources
        + 0.11 * p.communication
        + 0.10 * p.accountability
        + 0.10 * p.adaptation
}

fn main() {
    let profiles = vec![
        ImplementationProfile { name: "High-Intent Fragmented Organization", goal: 0.70, coordination: 0.38, structure: 0.44, culture: 0.31, incentives: 0.29, resources: 0.52, communication: 0.41, accountability: 0.46, adaptation: 0.36 },
        ImplementationProfile { name: "Balanced Aligned Organization", goal: 0.82, coordination: 0.81, structure: 0.79, culture: 0.78, incentives: 0.77, resources: 0.82, communication: 0.80, accountability: 0.76, adaptation: 0.74 },
        ImplementationProfile { name: "Adaptive Cross-Functional Organization", goal: 0.78, coordination: 0.84, structure: 0.73, culture: 0.76, incentives: 0.71, resources: 0.76, communication: 0.78, accountability: 0.74, adaptation: 0.83 },
    ];

    for p in profiles {
        println!("{} | implementation score {:.3}", p.name, implementation_score(&p));
    }
}
