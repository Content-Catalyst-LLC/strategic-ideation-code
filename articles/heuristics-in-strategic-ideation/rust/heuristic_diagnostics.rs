// Command-line heuristic diagnostics scaffold.
// Compile: rustc heuristic_diagnostics.rs -o heuristic_diagnostics
// Run: ./heuristic_diagnostics

#[derive(Debug)]
struct Context {
    id: &'static str,
    availability: f64,
    anchoring: f64,
    recognition: f64,
    satisficing: f64,
    affect: f64,
    default_gravity: f64,
    social_proof: f64,
    diversity: f64,
    stakeholder: f64,
    source_domain: f64,
    systems: f64,
    political: f64,
    memory: f64,
}

fn profile(c: &Context) -> f64 {
    -0.11 * c.availability
        - 0.11 * c.anchoring
        - 0.10 * c.recognition
        - 0.11 * c.satisficing
        - 0.07 * c.affect
        - 0.08 * c.default_gravity
        - 0.06 * c.social_proof
        + 0.17 * c.diversity
        + 0.13 * c.stakeholder
        + 0.13 * c.source_domain
        + 0.14 * c.systems
        + 0.07 * c.political
        + 0.08 * c.memory
}

fn closure_pressure(c: &Context) -> f64 {
    c.anchoring * c.satisficing
}

fn diagnosis(c: &Context) -> &'static str {
    if closure_pressure(c) >= 0.55 {
        "premature_closure_risk"
    } else if c.recognition * (1.0 - c.diversity) >= 0.50 {
        "recognition_trap_risk"
    } else if c.stakeholder < 0.35 {
        "stakeholder_visibility_gap"
    } else if profile(c) >= 0.20 {
        "stronger_heuristic_ecology"
    } else {
        "requires_heuristic_review"
    }
}

fn main() {
    let contexts = vec![
        Context { id: "H001", availability: 0.84, anchoring: 0.63, recognition: 0.79, satisficing: 0.82, affect: 0.66, default_gravity: 0.72, social_proof: 0.70, diversity: 0.29, stakeholder: 0.34, source_domain: 0.28, systems: 0.40, political: 0.48, memory: 0.34 },
        Context { id: "H004", availability: 0.31, anchoring: 0.27, recognition: 0.36, satisficing: 0.34, affect: 0.32, default_gravity: 0.30, social_proof: 0.28, diversity: 0.89, stakeholder: 0.82, source_domain: 0.88, systems: 0.78, political: 0.74, memory: 0.72 },
        Context { id: "H005", availability: 0.76, anchoring: 0.72, recognition: 0.82, satisficing: 0.78, affect: 0.62, default_gravity: 0.88, social_proof: 0.74, diversity: 0.30, stakeholder: 0.28, source_domain: 0.26, systems: 0.36, political: 0.30, memory: 0.36 },
    ];

    for context in contexts {
        println!(
            "{} | profile {:.3} | closure {:.3} | {}",
            context.id,
            profile(&context),
            closure_pressure(&context),
            diagnosis(&context)
        );
    }
}
