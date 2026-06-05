// Command-line journey diagnostics scaffold.
// Compile: rustc journey_diagnostics.rs -o journey_diagnostics
// Run: ./journey_diagnostics

#[derive(Debug)]
struct Journey {
    id: &'static str,
    clarity: f64,
    emotional_confidence: f64,
    friction: f64,
    transition_quality: f64,
    accessibility: f64,
    trust: f64,
    completion_support: f64,
    backstage_alignment: f64,
    measurement_quality: f64,
}

fn journey_profile(j: &Journey) -> f64 {
    0.15 * j.clarity
        + 0.12 * j.emotional_confidence
        - 0.18 * j.friction
        + 0.14 * j.transition_quality
        + 0.12 * j.accessibility
        + 0.12 * j.trust
        + 0.10 * j.completion_support
        + 0.10 * j.backstage_alignment
        + 0.07 * j.measurement_quality
}

fn redesign_need(j: &Journey) -> f64 {
    0.22 * j.friction
        + 0.16 * (1.0 - j.transition_quality)
        + 0.14 * (1.0 - j.accessibility)
        + 0.13 * (1.0 - j.trust)
        + 0.12 * (1.0 - j.clarity)
        + 0.11 * (1.0 - j.backstage_alignment)
        + 0.07 * (1.0 - j.completion_support)
        + 0.05 * (1.0 - j.measurement_quality)
}

fn recommendation(j: &Journey) -> &'static str {
    if journey_profile(j) >= 0.58 {
        "strong_experience_design_profile"
    } else if redesign_need(j) >= 0.62 {
        "high_redesign_priority"
    } else if j.transition_quality < 0.45 {
        "transition_and_handoff_failure"
    } else {
        "developing_journey_quality"
    }
}

fn main() {
    let journeys = vec![
        Journey { id: "J001", clarity: 0.36, emotional_confidence: 0.31, friction: 0.82, transition_quality: 0.28, accessibility: 0.34, trust: 0.30, completion_support: 0.34, backstage_alignment: 0.30, measurement_quality: 0.38 },
        Journey { id: "J005", clarity: 0.81, emotional_confidence: 0.79, friction: 0.28, transition_quality: 0.82, accessibility: 0.88, trust: 0.84, completion_support: 0.86, backstage_alignment: 0.78, measurement_quality: 0.76 },
        Journey { id: "J007", clarity: 0.54, emotional_confidence: 0.45, friction: 0.72, transition_quality: 0.36, accessibility: 0.50, trust: 0.44, completion_support: 0.52, backstage_alignment: 0.34, measurement_quality: 0.46 },
    ];

    for j in journeys {
        println!(
            "{} | journey profile {:.3} | redesign need {:.3} | {}",
            j.id,
            journey_profile(&j),
            redesign_need(&j),
            recommendation(&j)
        );
    }
}
