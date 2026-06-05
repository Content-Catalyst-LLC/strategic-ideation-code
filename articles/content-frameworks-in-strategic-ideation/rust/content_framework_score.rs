// Command-line content framework scoring scaffold.
// Compile: rustc content_framework_score.rs -o content_framework_score
// Run: ./content_framework_score

struct Framework {
    name: &'static str,
    structure: f64,
    clarity: f64,
    evidence: f64,
    assumptions: f64,
    narrative: f64,
    decision: f64,
    modularity: f64,
    reuse: f64,
    governance: f64,
    ethics: f64,
}

fn score(fw: &Framework) -> f64 {
    0.11 * fw.structure
        + 0.11 * fw.clarity
        + 0.12 * fw.evidence
        + 0.10 * fw.assumptions
        + 0.10 * fw.narrative
        + 0.13 * fw.decision
        + 0.10 * fw.modularity
        + 0.10 * fw.reuse
        + 0.08 * fw.governance
        + 0.05 * fw.ethics
}

fn main() {
    let frameworks = vec![
        Framework { name: "Idea Record Framework", structure: 0.76, clarity: 0.72, evidence: 0.66, assumptions: 0.68, narrative: 0.62, decision: 0.64, modularity: 0.74, reuse: 0.72, governance: 0.66, ethics: 0.60 },
        Framework { name: "Decision Memo Framework", structure: 0.82, clarity: 0.76, evidence: 0.80, assumptions: 0.78, narrative: 0.74, decision: 0.86, modularity: 0.66, reuse: 0.68, governance: 0.72, ethics: 0.72 },
        Framework { name: "AI-Assisted Ideation Framework", structure: 0.62, clarity: 0.56, evidence: 0.50, assumptions: 0.48, narrative: 0.58, decision: 0.54, modularity: 0.60, reuse: 0.58, governance: 0.46, ethics: 0.42 },
    ];

    for fw in frameworks {
        let value = score(&fw);
        println!("{} | framework strength {:.3} | framework risk {:.3}", fw.name, value, 1.0 - value);
    }
}
