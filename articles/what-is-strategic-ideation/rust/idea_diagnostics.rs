// Advanced command-line idea diagnostics scaffold.
// Compile: rustc idea_diagnostics.rs -o idea_diagnostics
// Run: ./idea_diagnostics

#[derive(Debug)]
struct IdeaDiagnostic {
    idea_id: &'static str,
    strategic_fit: f64,
    feasibility: f64,
    systems_leverage: f64,
    learning_value: f64,
    ethical_legitimacy: f64,
    knowledge_reusability: f64,
    uncertainty: f64,
    assumption_risk: f64,
}

fn score(item: &IdeaDiagnostic) -> f64 {
    0.20 * item.strategic_fit
        + 0.12 * item.feasibility
        + 0.18 * item.systems_leverage
        + 0.13 * item.learning_value
        + 0.16 * item.ethical_legitimacy
        + 0.09 * item.knowledge_reusability
        - 0.07 * item.uncertainty
        - 0.05 * item.assumption_risk
}

fn recommendation(item: &IdeaDiagnostic) -> &'static str {
    let s = score(item);
    if s >= 0.82 && item.assumption_risk < 0.30 {
        "advance_to_strategy_review"
    } else if s >= 0.74 {
        "prototype_or_test"
    } else if item.assumption_risk >= 0.42 {
        "test_assumptions_before_selection"
    } else {
        "hold_or_reframe"
    }
}

fn main() {
    let ideas = vec![
        IdeaDiagnostic { idea_id: "I001", strategic_fit: 0.91, feasibility: 0.82, systems_leverage: 0.74, learning_value: 0.88, ethical_legitimacy: 0.86, knowledge_reusability: 0.94, uncertainty: 0.24, assumption_risk: 0.29 },
        IdeaDiagnostic { idea_id: "I008", strategic_fit: 0.86, feasibility: 0.70, systems_leverage: 0.89, learning_value: 0.88, ethical_legitimacy: 0.87, knowledge_reusability: 0.84, uncertainty: 0.37, assumption_risk: 0.45 },
        IdeaDiagnostic { idea_id: "I012", strategic_fit: 0.85, feasibility: 0.64, systems_leverage: 0.84, learning_value: 0.94, ethical_legitimacy: 0.88, knowledge_reusability: 0.85, uncertainty: 0.39, assumption_risk: 0.44 },
    ];

    for idea in ideas {
        println!("{} | {:.3} | {}", idea.idea_id, score(&idea), recommendation(&idea));
    }
}
