// Command-line empathy diagnostics scaffold.
// Compile: rustc empathy_diagnostics.rs -o empathy_diagnostics
// Run: ./empathy_diagnostics

#[derive(Debug)]
struct Context {
    id: &'static str,
    observation: f64,
    projection: f64,
    unmet_need: f64,
    stakeholder_breadth: f64,
    reframing: f64,
    ethics: f64,
    systems: f64,
    decision: f64,
    memory: f64,
}

fn empathy_profile(c: &Context) -> f64 {
    0.16 * c.observation
        - 0.14 * c.projection
        + 0.16 * c.unmet_need
        + 0.12 * c.stakeholder_breadth
        + 0.16 * c.reframing
        + 0.10 * c.ethics
        + 0.10 * c.systems
        + 0.14 * c.decision
        + 0.10 * c.memory
}

fn superficiality_risk(c: &Context) -> f64 {
    0.20 * c.projection
        + 0.16 * (1.0 - c.decision)
        + 0.14 * (1.0 - c.observation)
        + 0.12 * (1.0 - c.unmet_need)
        + 0.12 * (1.0 - c.ethics)
        + 0.10 * (1.0 - c.systems)
        + 0.08 * (1.0 - c.stakeholder_breadth)
        + 0.08 * (1.0 - c.memory)
}

fn recommendation(c: &Context) -> &'static str {
    if empathy_profile(c) >= 0.64 {
        "strong_user_centered_ideation_capability"
    } else if superficiality_risk(c) >= 0.62 {
        "high_empathy_theater_or_projection_risk"
    } else if c.decision < 0.42 {
        "insight_not_linked_to_decisions"
    } else {
        "developing_capability"
    }
}

fn main() {
    let contexts = vec![
        Context { id: "C001", observation: 0.24, projection: 0.84, unmet_need: 0.31, stakeholder_breadth: 0.28, reframing: 0.34, ethics: 0.38, systems: 0.35, decision: 0.32, memory: 0.30 },
        Context { id: "C004", observation: 0.76, projection: 0.48, unmet_need: 0.79, stakeholder_breadth: 0.90, reframing: 0.83, ethics: 0.86, systems: 0.88, decision: 0.78, memory: 0.76 },
        Context { id: "C005", observation: 0.38, projection: 0.72, unmet_need: 0.42, stakeholder_breadth: 0.36, reframing: 0.40, ethics: 0.32, systems: 0.30, decision: 0.24, memory: 0.22 },
    ];

    for c in contexts {
        println!(
            "{} | empathy profile {:.3} | superficiality risk {:.3} | {}",
            c.id,
            empathy_profile(&c),
            superficiality_risk(&c),
            recommendation(&c)
        );
    }
}
