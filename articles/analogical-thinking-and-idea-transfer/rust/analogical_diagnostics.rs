// Command-line analogical transfer diagnostics scaffold.
// Compile: rustc analogical_diagnostics.rs -o analogical_diagnostics
// Run: ./analogical_diagnostics

#[derive(Debug)]
struct Strategy {
    id: &'static str,
    structural_fit: f64,
    functional_fit: f64,
    surface_distraction: f64,
    adaptation_quality: f64,
    context_sensitivity: f64,
    stakeholder_legitimacy: f64,
    dynamic_compatibility: f64,
    innovation_potential: f64,
    evidence_strength: f64,
}

fn analogy_profile(s: &Strategy) -> f64 {
    0.20 * s.structural_fit
        + 0.16 * s.functional_fit
        - 0.16 * s.surface_distraction
        + 0.16 * s.adaptation_quality
        + 0.12 * s.context_sensitivity
        + 0.08 * s.stakeholder_legitimacy
        + 0.08 * s.dynamic_compatibility
        + 0.12 * s.innovation_potential
        + 0.08 * s.evidence_strength
}

fn surface_risk(s: &Strategy) -> f64 {
    s.surface_distraction * (1.0 - s.structural_fit)
}

fn diagnosis(s: &Strategy) -> &'static str {
    if surface_risk(s) >= 0.50 {
        "surface_analogy_risk"
    } else if s.adaptation_quality < 0.45 {
        "weak_adaptation"
    } else if s.dynamic_compatibility < 0.50 {
        "dynamic_compatibility_gap"
    } else if s.stakeholder_legitimacy < 0.50 {
        "stakeholder_legitimacy_gap"
    } else if analogy_profile(s) >= 0.60 {
        "strong_transfer_candidate"
    } else {
        "requires_analogy_review"
    }
}

fn main() {
    let strategies = vec![
        Strategy { id: "A001", structural_fit: 0.28, functional_fit: 0.46, surface_distraction: 0.82, adaptation_quality: 0.34, context_sensitivity: 0.30, stakeholder_legitimacy: 0.38, dynamic_compatibility: 0.26, innovation_potential: 0.29, evidence_strength: 0.36 },
        Strategy { id: "A005", structural_fit: 0.89, functional_fit: 0.83, surface_distraction: 0.22, adaptation_quality: 0.86, context_sensitivity: 0.84, stakeholder_legitimacy: 0.78, dynamic_compatibility: 0.86, innovation_potential: 0.88, evidence_strength: 0.80 },
        Strategy { id: "A007", structural_fit: 0.82, functional_fit: 0.78, surface_distraction: 0.34, adaptation_quality: 0.80, context_sensitivity: 0.76, stakeholder_legitimacy: 0.82, dynamic_compatibility: 0.84, innovation_potential: 0.78, evidence_strength: 0.76 },
    ];

    for strategy in strategies {
        println!(
            "{} | profile {:.3} | surface risk {:.3} | {}",
            strategy.id,
            analogy_profile(&strategy),
            surface_risk(&strategy),
            diagnosis(&strategy)
        );
    }
}
