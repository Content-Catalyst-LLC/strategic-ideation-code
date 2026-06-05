// Command-line power distortion scoring scaffold.
// Compile: rustc power_distortion_score.rs -o power_distortion_score
// Run: ./power_distortion_score

struct PowerIdea {
    name: &'static str,
    merit: f64,
    evidence: f64,
    sponsorship: f64,
    resource_fit: f64,
    stakeholder: f64,
    dissent: f64,
    classification: f64,
    power_alignment: f64,
    advancement: f64,
}

fn merit_score(i: &PowerIdea) -> f64 {
    0.32*i.merit + 0.24*i.evidence + 0.18*i.stakeholder + 0.14*i.dissent + 0.12*i.classification
}

fn support_score(i: &PowerIdea) -> f64 {
    0.30*i.sponsorship + 0.25*i.resource_fit + 0.25*i.power_alignment + 0.20*i.advancement
}

fn main() {
    let ideas = vec![
        PowerIdea { name: "Participatory Governance Model", merit: 0.78, evidence: 0.72, sponsorship: 0.54, resource_fit: 0.58, stakeholder: 0.78, dissent: 0.72, classification: 0.76, power_alignment: 0.46, advancement: 0.52 },
        PowerIdea { name: "Executive Dashboard Expansion", merit: 0.62, evidence: 0.60, sponsorship: 0.86, resource_fit: 0.82, stakeholder: 0.42, dissent: 0.46, classification: 0.58, power_alignment: 0.84, advancement: 0.82 },
        PowerIdea { name: "Cost Consolidation Plan", merit: 0.58, evidence: 0.52, sponsorship: 0.82, resource_fit: 0.80, stakeholder: 0.34, dissent: 0.38, classification: 0.46, power_alignment: 0.86, advancement: 0.80 },
    ];

    for i in ideas {
        let merit = merit_score(&i);
        let support = support_score(&i);
        println!("{} | merit {:.3} | institutional support {:.3} | power distortion {:.3}", i.name, merit, support, support - merit);
    }
}
