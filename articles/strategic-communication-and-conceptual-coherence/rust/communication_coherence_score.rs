// Command-line communication coherence scoring scaffold.
// Compile: rustc communication_coherence_score.rs -o communication_coherence_score
// Run: ./communication_coherence_score

struct Profile {
    name: &'static str,
    concept: f64,
    narrative: f64,
    evidence: f64,
    audience: f64,
    decision: f64,
    implementation: f64,
    feedback: f64,
    governance: f64,
    ethics: f64,
}

fn score(p: &Profile) -> f64 {
    0.12 * p.concept
        + 0.12 * p.narrative
        + 0.13 * p.evidence
        + 0.10 * p.audience
        + 0.14 * p.decision
        + 0.12 * p.implementation
        + 0.08 * p.feedback
        + 0.10 * p.governance
        + 0.09 * p.ethics
}

fn main() {
    let profiles = vec![
        Profile { name: "Executive Strategy Briefing", concept: 0.74, narrative: 0.76, evidence: 0.72, audience: 0.70, decision: 0.82, implementation: 0.62, feedback: 0.58, governance: 0.70, ethics: 0.64 },
        Profile { name: "Stakeholder Explanation", concept: 0.68, narrative: 0.74, evidence: 0.70, audience: 0.82, decision: 0.66, implementation: 0.60, feedback: 0.78, governance: 0.66, ethics: 0.84 },
        Profile { name: "AI-Assisted Message Set", concept: 0.52, narrative: 0.58, evidence: 0.46, audience: 0.60, decision: 0.48, implementation: 0.46, feedback: 0.44, governance: 0.42, ethics: 0.40 },
    ];

    for p in profiles {
        let value = score(&p);
        println!("{} | coherence strength {:.3} | meaning loss risk {:.3}", p.name, value, 1.0 - value);
    }
}
