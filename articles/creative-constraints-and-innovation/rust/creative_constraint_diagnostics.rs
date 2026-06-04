// Command-line creative constraint diagnostics scaffold.
// Compile: rustc creative_constraint_diagnostics.rs -o creative_constraint_diagnostics
// Run: ./creative_constraint_diagnostics

#[derive(Debug)]
struct Context {
    id: &'static str,
    resource: f64,
    technical: f64,
    institutional: f64,
    ecological: f64,
    ethics: f64,
    focus: f64,
    opportunity: f64,
    legitimacy: f64,
    learning: f64,
    readiness: f64,
}

fn productive_profile(c: &Context) -> f64 {
    -0.10 * c.resource
        - 0.10 * c.technical
        - 0.10 * c.institutional
        + 0.12 * c.ecological
        + 0.16 * c.ethics
        + 0.16 * c.focus
        + 0.16 * c.opportunity
        + 0.14 * c.legitimacy
        + 0.14 * c.learning
        + 0.12 * c.readiness
}

fn rigidity_risk(c: &Context) -> f64 {
    let rigidity = 0.24 * c.resource + 0.25 * c.technical + 0.27 * c.institutional + 0.24 * c.ecological;
    rigidity * (1.0 - c.learning)
}

fn diffusion_risk(c: &Context) -> f64 {
    (1.0 - c.focus) * c.opportunity
}

fn diagnosis(c: &Context) -> &'static str {
    if diffusion_risk(c) >= 0.42 {
        "under_constrained_diffusion_risk"
    } else if rigidity_risk(c) >= 0.42 {
        "over_constrained_rigidity_risk"
    } else if c.legitimacy < 0.40 {
        "stakeholder_legitimacy_gap"
    } else if productive_profile(c) >= 0.42 {
        "productive_constraint_profile"
    } else {
        "requires_constraint_review"
    }
}

fn main() {
    let contexts = vec![
        Context { id: "CC001", resource: 0.12, technical: 0.18, institutional: 0.16, ecological: 0.20, ethics: 0.38, focus: 0.24, opportunity: 0.38, legitimacy: 0.42, learning: 0.36, readiness: 0.34 },
        Context { id: "CC002", resource: 0.54, technical: 0.47, institutional: 0.43, ecological: 0.52, ethics: 0.66, focus: 0.78, opportunity: 0.81, legitimacy: 0.72, learning: 0.78, readiness: 0.76 },
        Context { id: "CC007", resource: 0.66, technical: 0.52, institutional: 0.57, ecological: 0.92, ethics: 0.88, focus: 0.74, opportunity: 0.70, legitimacy: 0.82, learning: 0.76, readiness: 0.60 },
    ];

    for context in contexts {
        println!(
            "{} | profile {:.3} | rigidity {:.3} | diffusion {:.3} | {}",
            context.id,
            productive_profile(&context),
            rigidity_risk(&context),
            diffusion_risk(&context),
            diagnosis(&context)
        );
    }
}
