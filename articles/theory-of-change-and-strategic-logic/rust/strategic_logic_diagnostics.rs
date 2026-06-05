// Command-line strategic logic diagnostics scaffold.
// Compile: rustc strategic_logic_diagnostics.rs -o strategic_logic_diagnostics
// Run: ./strategic_logic_diagnostics

#[derive(Debug)]
struct Link {
    id: &'static str,
    mechanism_clarity: f64,
    evidence_strength: f64,
    actor_dependency: f64,
    capacity_dependency: f64,
    system_dependency: f64,
    ethical_dependency: f64,
    failure_consequence: f64,
    testability: f64,
}

fn link_risk(l: &Link) -> f64 {
    0.16 * (1.0 - l.mechanism_clarity)
        + 0.18 * (1.0 - l.evidence_strength)
        + 0.13 * l.actor_dependency
        + 0.11 * l.capacity_dependency
        + 0.14 * l.system_dependency
        + 0.12 * l.ethical_dependency
        + 0.16 * l.failure_consequence
}

fn test_priority(l: &Link) -> f64 {
    link_risk(l) * l.testability
}

fn recommendation(l: &Link) -> &'static str {
    if link_risk(l) >= 0.62 && l.testability >= 0.62 {
        "test_first"
    } else if link_risk(l) >= 0.62 {
        "reduce_commitment_before_scaling"
    } else if l.evidence_strength <= 0.42 {
        "evidence_gap"
    } else {
        "monitor"
    }
}

fn main() {
    let links = vec![
        Link { id: "L002", mechanism_clarity: 0.66, evidence_strength: 0.38, actor_dependency: 0.86, capacity_dependency: 0.62, system_dependency: 0.58, ethical_dependency: 0.52, failure_consequence: 0.80, testability: 0.78 },
        Link { id: "L004", mechanism_clarity: 0.72, evidence_strength: 0.44, actor_dependency: 0.82, capacity_dependency: 0.58, system_dependency: 0.68, ethical_dependency: 0.90, failure_consequence: 0.86, testability: 0.74 },
        Link { id: "L009", mechanism_clarity: 0.48, evidence_strength: 0.32, actor_dependency: 0.62, capacity_dependency: 0.48, system_dependency: 0.64, ethical_dependency: 0.60, failure_consequence: 0.78, testability: 0.58 },
    ];

    for link in links {
        println!(
            "{} | link risk {:.3} | test priority {:.3} | {}",
            link.id,
            link_risk(&link),
            test_priority(&link),
            recommendation(&link)
        );
    }
}
