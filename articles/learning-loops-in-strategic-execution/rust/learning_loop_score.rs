// Command-line learning loop scoring scaffold.
// Compile: rustc learning_loop_score.rs -o learning_loop_score
// Run: ./learning_loop_score

struct Context {
    name: &'static str,
    feedback: f64,
    assumptions: f64,
    interpretation: f64,
    authority: f64,
    closure: f64,
    memory: f64,
    safety: f64,
    scaling: f64,
    ethics: f64,
}

fn learning_score(c: &Context) -> f64 {
    0.13 * c.feedback
        + 0.13 * c.assumptions
        + 0.12 * c.interpretation
        + 0.14 * c.authority
        + 0.14 * c.closure
        + 0.10 * c.memory
        + 0.09 * c.safety
        + 0.08 * c.scaling
        + 0.07 * c.ethics
}

fn main() {
    let contexts = vec![
        Context { name: "Reporting-Heavy Organization", feedback: 0.62, assumptions: 0.42, interpretation: 0.46, authority: 0.38, closure: 0.34, memory: 0.36, safety: 0.44, scaling: 0.40, ethics: 0.50 },
        Context { name: "Adaptive Learning Organization", feedback: 0.84, assumptions: 0.82, interpretation: 0.80, authority: 0.78, closure: 0.82, memory: 0.76, safety: 0.78, scaling: 0.74, ethics: 0.80 },
        Context { name: "Pilot-Rich Memory-Poor Organization", feedback: 0.72, assumptions: 0.60, interpretation: 0.62, authority: 0.56, closure: 0.48, memory: 0.30, safety: 0.58, scaling: 0.36, ethics: 0.56 },
    ];

    for c in contexts {
        let score = learning_score(&c);
        println!("{} | learning loop strength {:.3} | learning debt {:.3}", c.name, score, 1.0 - score);
    }
}
