// Command-line knowledge architecture scoring scaffold.
// Compile: rustc knowledge_architecture_score.rs -o knowledge_architecture_score
// Run: ./knowledge_architecture_score

struct Idea {
    name: &'static str,
    taxonomy: f64,
    metadata: f64,
    semantics: f64,
    evidence: f64,
    assumptions: f64,
    relationships: f64,
    retrieval: f64,
    memory: f64,
    stewardship: f64,
    ethics: f64,
}

fn architecture_score(i: &Idea) -> f64 {
    0.11 * i.taxonomy
        + 0.12 * i.metadata
        + 0.11 * i.semantics
        + 0.12 * i.evidence
        + 0.11 * i.assumptions
        + 0.11 * i.relationships
        + 0.12 * i.retrieval
        + 0.09 * i.memory
        + 0.07 * i.stewardship
        + 0.04 * i.ethics
}

fn main() {
    let ideas = vec![
        Idea { name: "Community Data Stewardship", taxonomy: 0.74, metadata: 0.70, semantics: 0.76, evidence: 0.66, assumptions: 0.68, relationships: 0.72, retrieval: 0.70, memory: 0.62, stewardship: 0.64, ethics: 0.78 },
        Idea { name: "AI-Assisted Scenario Library", taxonomy: 0.62, metadata: 0.58, semantics: 0.54, evidence: 0.52, assumptions: 0.50, relationships: 0.58, retrieval: 0.54, memory: 0.46, stewardship: 0.48, ethics: 0.46 },
        Idea { name: "Strategic Learning Repository", taxonomy: 0.78, metadata: 0.80, semantics: 0.82, evidence: 0.74, assumptions: 0.72, relationships: 0.82, retrieval: 0.84, memory: 0.78, stewardship: 0.76, ethics: 0.66 },
    ];

    for i in ideas {
        let score = architecture_score(&i);
        println!("{} | architecture strength {:.3} | architecture risk {:.3}", i.name, score, 1.0 - score);
    }
}
