// Rust command-line idea diagnostics scaffold.
// Compile: rustc idea_diagnostics.rs -o idea_diagnostics
// Run: ./idea_diagnostics

#[derive(Debug)]
struct IdeaDiagnostic {
    idea_id: &'static str,
    strategic_fit: f64,
    feasibility: f64,
    systems_leverage: f64,
    assumption_risk: f64,
}

fn diagnostic_score(item: &IdeaDiagnostic) -> f64 {
    0.30 * item.strategic_fit
        + 0.20 * item.feasibility
        + 0.30 * item.systems_leverage
        - 0.20 * item.assumption_risk
}

fn main() {
    let ideas = vec![
        IdeaDiagnostic { idea_id: "I001", strategic_fit: 0.91, feasibility: 0.82, systems_leverage: 0.74, assumption_risk: 0.29 },
        IdeaDiagnostic { idea_id: "I003", strategic_fit: 0.87, feasibility: 0.71, systems_leverage: 0.81, assumption_risk: 0.31 },
        IdeaDiagnostic { idea_id: "I006", strategic_fit: 0.74, feasibility: 0.67, systems_leverage: 0.72, assumption_risk: 0.42 },
    ];

    for idea in ideas {
        let score = diagnostic_score(&idea);
        let flag = if score >= 0.72 { "advance" } else { "revise" };
        println!("{} | {:.3} | {}", idea.idea_id, score, flag);
    }
}
