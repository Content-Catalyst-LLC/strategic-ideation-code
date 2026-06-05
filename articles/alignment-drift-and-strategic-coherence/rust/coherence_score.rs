// Command-line strategic coherence scoring scaffold.
// Compile: rustc coherence_score.rs -o coherence_score
// Run: ./coherence_score

struct Context {
    name: &'static str,
    purpose: f64,
    priority: f64,
    tradeoff: f64,
    resources: f64,
    incentives: f64,
    interpretation: f64,
    governance: f64,
    feedback: f64,
    memory: f64,
    ethics: f64,
}

fn coherence_score(c: &Context) -> f64 {
    0.15 * c.purpose
        + 0.12 * c.priority
        + 0.11 * c.tradeoff
        + 0.13 * c.resources
        + 0.13 * c.incentives
        + 0.11 * c.interpretation
        + 0.12 * c.governance
        + 0.08 * c.feedback
        + 0.07 * c.memory
        + 0.08 * c.ethics
}

fn main() {
    let contexts = vec![
        Context { name: "Symbolically Aligned Organization", purpose: 0.64, priority: 0.50, tradeoff: 0.46, resources: 0.46, incentives: 0.42, interpretation: 0.50, governance: 0.44, feedback: 0.48, memory: 0.40, ethics: 0.54 },
        Context { name: "Coherent Adaptive Organization", purpose: 0.84, priority: 0.80, tradeoff: 0.78, resources: 0.78, incentives: 0.80, interpretation: 0.82, governance: 0.78, feedback: 0.84, memory: 0.76, ethics: 0.80 },
        Context { name: "Metric-Substituted Organization", purpose: 0.68, priority: 0.60, tradeoff: 0.54, resources: 0.62, incentives: 0.36, interpretation: 0.58, governance: 0.52, feedback: 0.44, memory: 0.50, ethics: 0.46 },
    ];

    for c in contexts {
        let score = coherence_score(&c);
        println!("{} | coherence {:.3} | drift risk {:.3}", c.name, score, 1.0 - score);
    }
}
