// Command-line institutional memory scoring scaffold.
// Compile: rustc institutional_memory_score.rs -o institutional_memory_score
// Run: ./institutional_memory_score

struct MemorySystem {
    name: &'static str,
    capture: f64,
    metadata: f64,
    context: f64,
    decisions: f64,
    learning: f64,
    retrieval: f64,
    reuse: f64,
    stewardship: f64,
    continuity: f64,
    ethics: f64,
}

fn score(m: &MemorySystem) -> f64 {
    0.10 * m.capture
        + 0.12 * m.metadata
        + 0.12 * m.context
        + 0.13 * m.decisions
        + 0.12 * m.learning
        + 0.12 * m.retrieval
        + 0.10 * m.reuse
        + 0.08 * m.stewardship
        + 0.06 * m.continuity
        + 0.05 * m.ethics
}

fn main() {
    let systems = vec![
        MemorySystem { name: "Strategic Idea Repository", capture: 0.72, metadata: 0.80, context: 0.76, decisions: 0.66, learning: 0.68, retrieval: 0.78, reuse: 0.80, stewardship: 0.72, continuity: 0.70, ethics: 0.62 },
        MemorySystem { name: "Decision Memory", capture: 0.70, metadata: 0.74, context: 0.82, decisions: 0.86, learning: 0.72, retrieval: 0.74, reuse: 0.76, stewardship: 0.70, continuity: 0.72, ethics: 0.70 },
        MemorySystem { name: "Retired Ideas Archive", capture: 0.58, metadata: 0.54, context: 0.56, decisions: 0.58, learning: 0.48, retrieval: 0.52, reuse: 0.60, stewardship: 0.50, continuity: 0.48, ethics: 0.58 },
    ];

    for m in systems {
        let value = score(&m);
        println!("{} | memory strength {:.3} | failure risk {:.3}", m.name, value, 1.0 - value);
    }
}
