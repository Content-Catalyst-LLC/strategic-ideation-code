// Command-line strategic creativity diagnostics scaffold.
// Compile: rustc creativity_diagnostics.rs -o creativity_diagnostics
// Run: ./creativity_diagnostics

#[derive(Debug)]
struct Idea {
    id: &'static str,
    novelty: f64,
    relevance: f64,
    coherence: f64,
    mechanism: f64,
    testability: f64,
    stakeholder: f64,
    systems: f64,
    development: f64,
    risk: f64,
    revision: f64,
}

fn score(i: &Idea) -> f64 {
    0.14 * i.novelty
        + 0.16 * i.relevance
        + 0.13 * i.coherence
        + 0.14 * i.mechanism
        + 0.11 * i.testability
        + 0.13 * i.stakeholder
        + 0.13 * i.systems
        + 0.12 * i.development
        + 0.08 * i.revision
        - 0.12 * i.risk
}

fn novelty_theater_risk(i: &Idea) -> f64 {
    i.novelty * (1.0 - ((i.mechanism + i.stakeholder + i.systems) / 3.0))
}

fn recommendation(i: &Idea) -> &'static str {
    if novelty_theater_risk(i) >= 0.42 {
        "novelty_theater_review"
    } else if i.stakeholder < 0.45 {
        "stakeholder_grounding_review"
    } else if i.systems < 0.50 {
        "systems_fit_review"
    } else if score(i) >= 0.70 {
        "strong_strategic_creativity_candidate"
    } else {
        "develop_with_testing"
    }
}

fn main() {
    let ideas = vec![
        Idea { id: "I002", novelty: 0.72, relevance: 0.86, coherence: 0.78, mechanism: 0.80, testability: 0.70, stakeholder: 0.92, systems: 0.78, development: 0.82, risk: 0.56, revision: 0.82 },
        Idea { id: "I005", novelty: 0.76, relevance: 0.88, coherence: 0.82, mechanism: 0.84, testability: 0.66, stakeholder: 0.70, systems: 0.90, development: 0.86, risk: 0.66, revision: 0.86 },
        Idea { id: "I009", novelty: 0.70, relevance: 0.50, coherence: 0.52, mechanism: 0.34, testability: 0.46, stakeholder: 0.30, systems: 0.32, development: 0.42, risk: 0.40, revision: 0.38 },
    ];

    for idea in ideas {
        println!(
            "{} | score {:.3} | novelty-theater-risk {:.3} | {}",
            idea.id,
            score(&idea),
            novelty_theater_risk(&idea),
            recommendation(&idea)
        );
    }
}
