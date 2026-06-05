// Command-line opportunity profile scoring scaffold.
// Compile: rustc opportunity_score.rs -o opportunity_score
// Run: ./opportunity_score

#[derive(Debug)]
struct OpportunityProfile {
    name: &'static str,
    signal: f64,
    capability: f64,
    desirability: f64,
    viability: f64,
    timing: f64,
    learning: f64,
    option_value: f64,
    strategic_fit: f64,
    ethics: f64,
    risk: f64,
    confidence: f64,
}

fn profile_score(o: &OpportunityProfile) -> f64 {
    0.13 * o.signal
        + 0.14 * o.capability
        + 0.12 * o.desirability
        + 0.12 * o.viability
        + 0.10 * o.timing
        + 0.12 * o.learning
        + 0.11 * o.option_value
        + 0.10 * o.strategic_fit
        + 0.10 * o.ethics
        - 0.14 * o.risk
}

fn main() {
    let opportunities = vec![
        OpportunityProfile { name: "Emerging Technology Adjacency", signal: 0.74, capability: 0.78, desirability: 0.72, viability: 0.71, timing: 0.76, learning: 0.70, option_value: 0.66, strategic_fit: 0.78, ethics: 0.62, risk: 0.46, confidence: 0.68 },
        OpportunityProfile { name: "High-Hype Weak-Fit Opportunity", signal: 0.86, capability: 0.31, desirability: 0.77, viability: 0.39, timing: 0.48, learning: 0.62, option_value: 0.44, strategic_fit: 0.40, ethics: 0.42, risk: 0.78, confidence: 0.38 },
        OpportunityProfile { name: "Slow-Build Sustainability Opportunity", signal: 0.62, capability: 0.73, desirability: 0.81, viability: 0.74, timing: 0.67, learning: 0.64, option_value: 0.72, strategic_fit: 0.76, ethics: 0.82, risk: 0.41, confidence: 0.66 },
    ];

    for o in opportunities {
        let score = profile_score(&o);
        println!("{} | score {:.3} | confidence-adjusted {:.3}", o.name, score, score * o.confidence);
    }
}
