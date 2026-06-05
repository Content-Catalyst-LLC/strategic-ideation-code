// Command-line future-ready strategic ideation scoring scaffold.
// Compile: rustc future_ideation_score.rs -o future_ideation_score
// Run: ./future_ideation_score

struct FutureIdea {
    name: &'static str,
    frame: f64,
    evidence: f64,
    adaptability: f64,
    scenario: f64,
    stakeholder: f64,
    implementation: f64,
    ethics: f64,
    learning: f64,
    option_value: f64,
    ai: f64,
}

fn future_ready_score(i: &FutureIdea) -> f64 {
    0.11*i.frame + 0.11*i.evidence + 0.11*i.adaptability + 0.12*i.scenario +
    0.11*i.stakeholder + 0.10*i.implementation + 0.11*i.ethics + 0.12*i.learning +
    0.07*i.option_value + 0.04*i.ai
}

fn main() {
    let ideas = vec![
        FutureIdea { name: "Scenario-Linked Option Portfolio", frame: 0.78, evidence: 0.72, adaptability: 0.84, scenario: 0.86, stakeholder: 0.70, implementation: 0.70, ethics: 0.76, learning: 0.86, option_value: 0.90, ai: 0.62 },
        FutureIdea { name: "Participatory Strategy Lab", frame: 0.80, evidence: 0.74, adaptability: 0.78, scenario: 0.72, stakeholder: 0.86, implementation: 0.64, ethics: 0.84, learning: 0.78, option_value: 0.72, ai: 0.56 },
        FutureIdea { name: "Rapid Automation Initiative", frame: 0.54, evidence: 0.52, adaptability: 0.48, scenario: 0.46, stakeholder: 0.42, implementation: 0.50, ethics: 0.44, learning: 0.42, option_value: 0.46, ai: 0.38 },
    ];

    for i in ideas {
        let value = future_ready_score(&i);
        println!("{} | future-ready score {:.3} | future risk {:.3}", i.name, value, 1.0 - value);
    }
}
