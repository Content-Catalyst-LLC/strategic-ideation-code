// Command-line divergence-convergence diagnostics scaffold.
// Compile: rustc divergence_convergence_diagnostics.rs -o divergence_convergence_diagnostics
// Run: ./divergence_convergence_diagnostics

#[derive(Debug)]
struct Context {
    id: &'static str,
    exploratory_breadth: f64,
    evaluative_discipline: f64,
    iteration_quality: f64,
    constraint_clarity: f64,
    stakeholder_inclusion: f64,
    evidence_contact: f64,
    action_readiness: f64,
    decision_memory_quality: f64,
    closure_pressure: f64,
}

fn profile_score(c: &Context) -> f64 {
    0.16 * c.exploratory_breadth
        + 0.16 * c.evaluative_discipline
        + 0.18 * c.iteration_quality
        + 0.14 * c.constraint_clarity
        + 0.12 * c.stakeholder_inclusion
        + 0.12 * c.evidence_contact
        + 0.08 * c.action_readiness
        + 0.04 * c.decision_memory_quality
}

fn premature_convergence_risk(c: &Context) -> f64 {
    (1.0 - c.exploratory_breadth) * c.closure_pressure
}

fn unbounded_divergence_risk(c: &Context) -> f64 {
    c.exploratory_breadth * (1.0 - c.evaluative_discipline)
}

fn diagnosis(c: &Context) -> &'static str {
    if premature_convergence_risk(c) >= 0.55 {
        "premature_convergence_risk"
    } else if unbounded_divergence_risk(c) >= 0.55 {
        "unbounded_divergence_risk"
    } else if profile_score(c) >= 0.70 {
        "balanced_and_adaptive"
    } else {
        "requires_process_review"
    }
}

fn main() {
    let contexts = vec![
        Context { id: "DC001", exploratory_breadth: 0.28, evaluative_discipline: 0.86, iteration_quality: 0.31, constraint_clarity: 0.71, stakeholder_inclusion: 0.34, evidence_contact: 0.42, action_readiness: 0.79, decision_memory_quality: 0.38, closure_pressure: 0.88 },
        Context { id: "DC002", exploratory_breadth: 0.74, evaluative_discipline: 0.77, iteration_quality: 0.76, constraint_clarity: 0.73, stakeholder_inclusion: 0.70, evidence_contact: 0.74, action_readiness: 0.81, decision_memory_quality: 0.72, closure_pressure: 0.62 },
        Context { id: "DC003", exploratory_breadth: 0.91, evaluative_discipline: 0.22, iteration_quality: 0.38, constraint_clarity: 0.19, stakeholder_inclusion: 0.46, evidence_contact: 0.31, action_readiness: 0.27, decision_memory_quality: 0.30, closure_pressure: 0.22 },
    ];

    for context in contexts {
        println!(
            "{} | profile {:.3} | premature {:.3} | unbounded {:.3} | {}",
            context.id,
            profile_score(&context),
            premature_convergence_risk(&context),
            unbounded_divergence_risk(&context),
            diagnosis(&context)
        );
    }
}
