// Command-line sequencing readiness scoring scaffold.
// Compile: rustc sequencing_score.rs -o sequencing_score
// Run: ./sequencing_score

struct Pathway {
    name: &'static str,
    capability: f64,
    evidence: f64,
    governance: f64,
    legitimacy: f64,
    dependency: f64,
    reversibility: f64,
    capacity: f64,
    timing: f64,
    ethics: f64,
}

fn sequencing_readiness(p: &Pathway) -> f64 {
    0.16 * p.capability
        + 0.15 * p.evidence
        + 0.15 * p.governance
        + 0.14 * p.legitimacy
        - 0.12 * p.dependency
        + 0.10 * p.reversibility
        - 0.10 * p.capacity
        + 0.08 * p.timing
        + 0.12 * p.ethics
}

fn main() {
    let pathways = vec![
        Pathway { name: "Data Governance Foundation", capability: 0.72, evidence: 0.66, governance: 0.78, legitimacy: 0.62, dependency: 0.42, reversibility: 0.70, capacity: 0.46, timing: 0.52, ethics: 0.70 },
        Pathway { name: "Full Platform Rollout", capability: 0.52, evidence: 0.46, governance: 0.48, legitimacy: 0.44, dependency: 0.82, reversibility: 0.38, capacity: 0.84, timing: 0.60, ethics: 0.42 },
        Pathway { name: "Adaptive Rollout Sequence", capability: 0.70, evidence: 0.68, governance: 0.72, legitimacy: 0.74, dependency: 0.52, reversibility: 0.76, capacity: 0.60, timing: 0.66, ethics: 0.78 },
    ];

    for p in pathways {
        println!("{} | sequencing readiness {:.3}", p.name, sequencing_readiness(&p));
    }
}
