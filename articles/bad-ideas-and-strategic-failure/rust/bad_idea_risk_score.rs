// Command-line bad-idea risk scoring scaffold.
// Compile: rustc bad_idea_risk_score.rs -o bad_idea_risk_score
// Run: ./bad_idea_risk_score

struct BadIdea {
    name: &'static str,
    frame: f64,
    mechanism: f64,
    evidence: f64,
    implementation: f64,
    incentive: f64,
    ethics: f64,
    support: f64,
    merit: f64,
    learning: f64,
}

fn risk(i: &BadIdea) -> f64 {
    let distortion = (i.support - i.merit).max(0.0);
    0.14*(1.0-i.frame) + 0.12*(1.0-i.mechanism) + 0.15*(1.0-i.evidence) +
    0.14*(1.0-i.implementation) + 0.12*(1.0-i.incentive) + 0.12*(1.0-i.ethics) +
    0.11*(1.0-i.learning) + 0.10*distortion
}

fn main() {
    let ideas = vec![
        BadIdea { name: "AI-Assisted Workflow Redesign", frame: 0.54, mechanism: 0.56, evidence: 0.52, implementation: 0.48, incentive: 0.44, ethics: 0.46, support: 0.78, merit: 0.58, learning: 0.46 },
        BadIdea { name: "Cost Consolidation Plan", frame: 0.50, mechanism: 0.52, evidence: 0.48, implementation: 0.44, incentive: 0.36, ethics: 0.38, support: 0.82, merit: 0.54, learning: 0.40 },
        BadIdea { name: "Reversible Pilot Portfolio", frame: 0.74, mechanism: 0.72, evidence: 0.70, implementation: 0.72, incentive: 0.68, ethics: 0.70, support: 0.58, merit: 0.78, learning: 0.82 },
    ];

    for i in ideas {
        let value = risk(&i);
        println!("{} | bad-idea risk {:.3}", i.name, value);
    }
}
