// Command-line leverage diagnostics scaffold.
// Compile: rustc leverage_diagnostics.rs -o leverage_diagnostics
// Run: ./leverage_diagnostics

#[derive(Debug)]
struct LeveragePoint {
    id: &'static str,
    implementation_ease: f64,
    structural_depth: f64,
    system_sensitivity: f64,
    feedback_influence: f64,
    information_effect: f64,
    rule_power: f64,
    goal_alignment: f64,
    paradigm_relevance: f64,
    transformative_potential: f64,
    legitimacy_requirement: f64,
    unintended_risk: f64,
    learning_capacity: f64,
}

fn leverage_score(l: &LeveragePoint) -> f64 {
    0.06 * l.implementation_ease
        + 0.16 * l.structural_depth
        + 0.14 * l.system_sensitivity
        + 0.13 * l.feedback_influence
        + 0.11 * l.information_effect
        + 0.13 * l.rule_power
        + 0.13 * l.goal_alignment
        + 0.08 * l.paradigm_relevance
        + 0.14 * l.transformative_potential
        + 0.08 * l.learning_capacity
        - 0.06 * l.unintended_risk
}

fn governance_need(l: &LeveragePoint) -> f64 {
    0.26 * l.legitimacy_requirement
        + 0.24 * l.unintended_risk
        + 0.22 * l.transformative_potential
        + 0.14 * (1.0 - l.implementation_ease)
        + 0.14 * l.paradigm_relevance
}

fn recommendation(l: &LeveragePoint) -> &'static str {
    if leverage_score(l) >= 0.72 && governance_need(l) >= 0.68 {
        "high_leverage_high_governance_need"
    } else if leverage_score(l) >= 0.68 {
        "high_leverage_candidate"
    } else if l.implementation_ease >= 0.70 && l.structural_depth <= 0.45 {
        "easy_but_shallow"
    } else {
        "moderate_leverage_review"
    }
}

fn main() {
    let points = vec![
        LeveragePoint { id: "L001", implementation_ease: 0.86, structural_depth: 0.22, system_sensitivity: 0.28, feedback_influence: 0.28, information_effect: 0.31, rule_power: 0.20, goal_alignment: 0.28, paradigm_relevance: 0.16, transformative_potential: 0.24, legitimacy_requirement: 0.24, unintended_risk: 0.26, learning_capacity: 0.34 },
        LeveragePoint { id: "L006", implementation_ease: 0.44, structural_depth: 0.82, system_sensitivity: 0.82, feedback_influence: 0.76, information_effect: 0.66, rule_power: 0.90, goal_alignment: 0.78, paradigm_relevance: 0.58, transformative_potential: 0.82, legitimacy_requirement: 0.72, unintended_risk: 0.70, learning_capacity: 0.70 },
        LeveragePoint { id: "L008", implementation_ease: 0.21, structural_depth: 0.96, system_sensitivity: 0.88, feedback_influence: 0.82, information_effect: 0.60, rule_power: 0.78, goal_alignment: 0.96, paradigm_relevance: 0.98, transformative_potential: 0.96, legitimacy_requirement: 0.90, unintended_risk: 0.82, learning_capacity: 0.78 },
    ];

    for point in points {
        println!(
            "{} | leverage {:.3} | governance need {:.3} | {}",
            point.id,
            leverage_score(&point),
            governance_need(&point),
            recommendation(&point)
        );
    }
}
