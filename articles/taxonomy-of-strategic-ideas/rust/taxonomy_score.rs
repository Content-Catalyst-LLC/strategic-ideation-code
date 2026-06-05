// Command-line taxonomy scoring scaffold.
// Compile: rustc taxonomy_score.rs -o taxonomy_score
// Run: ./taxonomy_score

struct TaxonomyRecord {
    name: &'static str,
    category: f64,
    level: f64,
    maturity: f64,
    evidence: f64,
    function: f64,
    relationships: f64,
    retrieval: f64,
    governance: f64,
    ethics: f64,
}

fn score(t: &TaxonomyRecord) -> f64 {
    0.13 * t.category
        + 0.11 * t.level
        + 0.11 * t.maturity
        + 0.12 * t.evidence
        + 0.13 * t.function
        + 0.11 * t.relationships
        + 0.13 * t.retrieval
        + 0.09 * t.governance
        + 0.07 * t.ethics
}

fn main() {
    let records = vec![
        TaxonomyRecord { name: "Strategic Learning Repository", category: 0.78, level: 0.76, maturity: 0.72, evidence: 0.72, function: 0.80, relationships: 0.76, retrieval: 0.82, governance: 0.74, ethics: 0.66 },
        TaxonomyRecord { name: "Participatory Governance Prototype", category: 0.76, level: 0.74, maturity: 0.76, evidence: 0.70, function: 0.74, relationships: 0.72, retrieval: 0.76, governance: 0.70, ethics: 0.82 },
        TaxonomyRecord { name: "Advisory Panel Without Authority", category: 0.66, level: 0.62, maturity: 0.72, evidence: 0.62, function: 0.60, relationships: 0.66, retrieval: 0.62, governance: 0.56, ethics: 0.76 },
    ];

    for t in records {
        let value = score(&t);
        println!("{} | taxonomy strength {:.3} | taxonomy risk {:.3}", t.name, value, 1.0 - value);
    }
}
