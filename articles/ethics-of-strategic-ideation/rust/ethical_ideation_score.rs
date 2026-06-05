// Command-line ethical ideation scoring scaffold.
// Compile: rustc ethical_ideation_score.rs -o ethical_ideation_score
// Run: ./ethical_ideation_score

struct EthicalIdea {
    name: &'static str,
    voice: f64,
    evidence: f64,
    burden: f64,
    uncertainty: f64,
    reversibility: f64,
    long_term: f64,
    ai: f64,
    accountability: f64,
    redress: f64,
}

fn legitimacy(i: &EthicalIdea) -> f64 {
    0.14*i.voice + 0.14*i.evidence + 0.12*i.burden + 0.11*i.uncertainty +
    0.10*i.reversibility + 0.13*i.long_term + 0.08*i.ai + 0.10*i.accountability + 0.08*i.redress
}

fn main() {
    let ideas = vec![
        EthicalIdea { name: "AI-Assisted Service Triage", voice: 0.42, evidence: 0.56, burden: 0.44, uncertainty: 0.46, reversibility: 0.50, long_term: 0.52, ai: 0.38, accountability: 0.48, redress: 0.36 },
        EthicalIdea { name: "Participatory Governance Council", voice: 0.84, evidence: 0.72, burden: 0.78, uncertainty: 0.70, reversibility: 0.72, long_term: 0.74, ai: 0.62, accountability: 0.76, redress: 0.72 },
        EthicalIdea { name: "Workforce Restructuring Plan", voice: 0.38, evidence: 0.58, burden: 0.40, uncertainty: 0.44, reversibility: 0.36, long_term: 0.42, ai: 0.40, accountability: 0.46, redress: 0.34 },
    ];

    for i in ideas {
        let value = legitimacy(&i);
        println!("{} | ethical legitimacy {:.3} | ethical risk {:.3}", i.name, value, 1.0 - value);
    }
}
