// Command-line design thinking diagnostics scaffold.
// Compile: rustc design_diagnostics.rs -o design_diagnostics
// Run: ./design_diagnostics

#[derive(Debug)]
struct DesignContext {
    id: &'static str,
    empathy: f64,
    reframing: f64,
    divergence: f64,
    convergence: f64,
    prototyping: f64,
    testing: f64,
    systems: f64,
    ethics: f64,
    decision: f64,
    adaptability: f64,
    memory: f64,
}

fn capability(c: &DesignContext) -> f64 {
    0.12 * c.empathy
        + 0.13 * c.reframing
        + 0.10 * c.divergence
        + 0.10 * c.convergence
        + 0.12 * c.prototyping
        + 0.12 * c.testing
        + 0.11 * c.systems
        + 0.10 * c.ethics
        + 0.10 * c.decision
        + 0.06 * c.adaptability
        + 0.04 * c.memory
}

fn superficiality_risk(c: &DesignContext) -> f64 {
    0.18 * (1.0 - c.empathy)
        + 0.14 * (1.0 - c.reframing)
        + 0.12 * (1.0 - c.testing)
        + 0.12 * (1.0 - c.systems)
        + 0.12 * (1.0 - c.ethics)
        + 0.16 * (1.0 - c.decision)
        + 0.10 * (1.0 - c.memory)
        + 0.06 * (1.0 - c.adaptability)
}

fn recommendation(c: &DesignContext) -> &'static str {
    if capability(c) >= 0.72 {
        "strong_design_thinking_capability"
    } else if superficiality_risk(c) >= 0.62 {
        "high_superficiality_risk"
    } else if c.decision < 0.45 {
        "weak_decision_linkage"
    } else {
        "developing_capability"
    }
}

fn main() {
    let contexts = vec![
        DesignContext { id: "C001", empathy: 0.28, reframing: 0.31, divergence: 0.36, convergence: 0.58, prototyping: 0.24, testing: 0.29, systems: 0.35, ethics: 0.42, decision: 0.36, adaptability: 0.33, memory: 0.40 },
        DesignContext { id: "C003", empathy: 0.81, reframing: 0.84, divergence: 0.86, convergence: 0.74, prototyping: 0.88, testing: 0.86, systems: 0.72, ethics: 0.74, decision: 0.78, adaptability: 0.89, memory: 0.76 },
        DesignContext { id: "C004", empathy: 0.39, reframing: 0.34, divergence: 0.68, convergence: 0.38, prototyping: 0.41, testing: 0.36, systems: 0.30, ethics: 0.34, decision: 0.28, adaptability: 0.42, memory: 0.24 },
    ];

    for c in contexts {
        println!(
            "{} | capability {:.3} | superficiality risk {:.3} | {}",
            c.id,
            capability(&c),
            superficiality_risk(&c),
            recommendation(&c)
        );
    }
}
