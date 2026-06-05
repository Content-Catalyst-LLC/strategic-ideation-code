// Command-line strategic portfolio scoring scaffold.
// Compile: rustc portfolio_score.rs -o portfolio_score
// Run: ./portfolio_score

#[derive(Debug)]
struct IdeaProfile {
    name: &'static str,
    impact: f64,
    risk: f64,
    learning: f64,
    option_value: f64,
    strategic_fit: f64,
    capacity_demand: f64,
    ethical_resilience: f64,
}

fn portfolio_contribution(i: &IdeaProfile) -> f64 {
    0.18 * i.impact
        + 0.18 * i.strategic_fit
        + 0.16 * i.learning
        + 0.16 * i.option_value
        + 0.14 * i.ethical_resilience
        - 0.10 * i.risk
        - 0.08 * i.capacity_demand
}

fn overload_warning(i: &IdeaProfile) -> f64 {
    0.34 * i.capacity_demand
        + 0.24 * i.risk
        + 0.16 * (1.0 - i.strategic_fit)
        + 0.14 * (1.0 - i.ethical_resilience)
        + 0.12 * (1.0 - i.option_value)
}

fn main() {
    let ideas = vec![
        IdeaProfile { name: "Core Process Improvement", impact: 0.68, risk: 0.32, learning: 0.38, option_value: 0.34, strategic_fit: 0.72, capacity_demand: 0.44, ethical_resilience: 0.58 },
        IdeaProfile { name: "Exploratory Market Experiment", impact: 0.58, risk: 0.56, learning: 0.84, option_value: 0.76, strategic_fit: 0.62, capacity_demand: 0.38, ethical_resilience: 0.62 },
        IdeaProfile { name: "Transformational Strategic Bet", impact: 0.88, risk: 0.78, learning: 0.70, option_value: 0.62, strategic_fit: 0.70, capacity_demand: 0.86, ethical_resilience: 0.48 },
    ];

    for idea in ideas {
        println!(
            "{} | contribution {:.3} | overload warning {:.3}",
            idea.name,
            portfolio_contribution(&idea),
            overload_warning(&idea)
        );
    }
}
