// Command-line complexity diagnostics scaffold.
// Compile: rustc complexity_diagnostics.rs -o complexity_diagnostics
// Run: ./complexity_diagnostics

#[derive(Debug)]
struct Environment {
    id: &'static str,
    interdependence: f64,
    nonlinearity: f64,
    feedback: f64,
    adaptation: f64,
    path: f64,
    boundary: f64,
    emergence: f64,
    deep_uncertainty: f64,
    scenario_need: f64,
    learning_need: f64,
}

fn complexity_score(e: &Environment) -> f64 {
    0.13 * e.interdependence
        + 0.13 * e.nonlinearity
        + 0.14 * e.feedback
        + 0.12 * e.adaptation
        + 0.11 * e.path
        + 0.10 * e.boundary
        + 0.10 * e.emergence
        + 0.09 * e.deep_uncertainty
        + 0.09 * e.scenario_need
        + 0.09 * e.learning_need
}

fn linear_planning_risk(e: &Environment) -> f64 {
    0.20 * e.nonlinearity
        + 0.20 * e.feedback
        + 0.18 * e.adaptation
        + 0.16 * e.deep_uncertainty
        + 0.14 * e.boundary
        + 0.12 * e.emergence
}

fn recommendation(e: &Environment) -> &'static str {
    if complexity_score(e) >= 0.76 {
        "adaptive_scenario_strategy_required"
    } else if complexity_score(e) >= 0.60 {
        "complexity_aware_strategy_recommended"
    } else if linear_planning_risk(e) >= 0.58 {
        "linear_planning_risk"
    } else {
        "standard_planning_may_be_sufficient"
    }
}

fn main() {
    let environments = vec![
        Environment { id: "ENV001", interdependence: 0.32, nonlinearity: 0.24, feedback: 0.31, adaptation: 0.28, path: 0.36, boundary: 0.30, emergence: 0.26, deep_uncertainty: 0.28, scenario_need: 0.30, learning_need: 0.34 },
        Environment { id: "ENV003", interdependence: 0.81, nonlinearity: 0.74, feedback: 0.79, adaptation: 0.71, path: 0.78, boundary: 0.76, emergence: 0.74, deep_uncertainty: 0.82, scenario_need: 0.82, learning_need: 0.80 },
        Environment { id: "ENV004", interdependence: 0.88, nonlinearity: 0.86, feedback: 0.87, adaptation: 0.82, path: 0.84, boundary: 0.82, emergence: 0.86, deep_uncertainty: 0.90, scenario_need: 0.90, learning_need: 0.88 },
    ];

    for environment in environments {
        println!(
            "{} | complexity {:.3} | linear planning risk {:.3} | {}",
            environment.id,
            complexity_score(&environment),
            linear_planning_risk(&environment),
            recommendation(&environment)
        );
    }
}
