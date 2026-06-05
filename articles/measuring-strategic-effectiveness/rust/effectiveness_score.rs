// Command-line strategic effectiveness scoring scaffold.
// Compile: rustc effectiveness_score.rs -o effectiveness_score
// Run: ./effectiveness_score

struct Strategy {
    name: &'static str,
    performance: f64,
    alignment: f64,
    resilience: f64,
    adaptability: f64,
    impact: f64,
    learning: f64,
    confidence: f64,
    ethics: f64,
}

fn effectiveness_score(s: &Strategy) -> f64 {
    0.20 * s.performance
        + 0.15 * s.alignment
        + 0.16 * s.resilience
        + 0.15 * s.adaptability
        + 0.14 * s.impact
        + 0.10 * s.learning
        + 0.05 * s.confidence
        + 0.05 * s.ethics
}

fn main() {
    let strategies = vec![
        Strategy { name: "Efficiency-Led Strategy", performance: 0.84, alignment: 0.58, resilience: 0.42, adaptability: 0.46, impact: 0.51, learning: 0.42, confidence: 0.66, ethics: 0.48 },
        Strategy { name: "Balanced Capability Strategy", performance: 0.72, alignment: 0.79, resilience: 0.76, adaptability: 0.78, impact: 0.73, learning: 0.76, confidence: 0.74, ethics: 0.72 },
        Strategy { name: "Adaptive Learning Strategy", performance: 0.70, alignment: 0.76, resilience: 0.78, adaptability: 0.88, impact: 0.74, learning: 0.90, confidence: 0.70, ethics: 0.76 },
    ];

    for s in strategies {
        let score = effectiveness_score(&s);
        println!("{} | score {:.3} | confidence-adjusted {:.3}", s.name, score, score * s.confidence);
    }
}
