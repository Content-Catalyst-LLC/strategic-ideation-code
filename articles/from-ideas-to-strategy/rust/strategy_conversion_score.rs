// Command-line idea-to-strategy conversion scoring scaffold.
// Compile: rustc strategy_conversion_score.rs -o strategy_conversion_score
// Run: ./strategy_conversion_score

#[derive(Debug)]
struct Initiative {
    name: &'static str,
    feasibility: f64,
    viability: f64,
    desirability: f64,
    integration_difficulty: f64,
    execution_readiness: f64,
    strategic_fit: f64,
    evidence_confidence: f64,
    ethical_resilience: f64,
}

fn conversion_score(i: &Initiative) -> f64 {
    0.16 * i.feasibility
        + 0.18 * i.viability
        + 0.16 * i.desirability
        - 0.12 * i.integration_difficulty
        + 0.16 * i.execution_readiness
        + 0.12 * i.strategic_fit
        + 0.08 * i.evidence_confidence
        + 0.06 * i.ethical_resilience
}

fn main() {
    let initiatives = vec![
        Initiative { name: "High-Idea Low-Execution Concept", feasibility: 0.78, viability: 0.38, desirability: 0.82, integration_difficulty: 0.72, execution_readiness: 0.29, strategic_fit: 0.62, evidence_confidence: 0.42, ethical_resilience: 0.54 },
        Initiative { name: "Balanced Strategic Initiative", feasibility: 0.74, viability: 0.79, desirability: 0.77, integration_difficulty: 0.44, execution_readiness: 0.81, strategic_fit: 0.84, evidence_confidence: 0.76, ethical_resilience: 0.72 },
        Initiative { name: "Integration-Challenged Initiative", feasibility: 0.69, viability: 0.71, desirability: 0.84, integration_difficulty: 0.83, execution_readiness: 0.52, strategic_fit: 0.76, evidence_confidence: 0.58, ethical_resilience: 0.60 },
    ];

    for i in initiatives {
        let score = conversion_score(&i);
        println!("{} | score {:.3} | confidence-adjusted {:.3}", i.name, score, score * i.evidence_confidence);
    }
}
