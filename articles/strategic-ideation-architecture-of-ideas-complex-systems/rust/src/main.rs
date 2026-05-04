fn weighted_score(values: &[f64], weights: &[f64]) -> f64 {
    values.iter().zip(weights.iter()).map(|(v, w)| v * w).sum()
}

fn main() {
    let values = vec![0.62, 0.86, 0.68, 0.88, 0.74, 0.35, 0.63];
    let weights = vec![0.16, 0.20, 0.16, 0.20, 0.14, -0.08, 0.14];

    println!("Strategic Ideation CLI");
    println!("Synthetic idea score: {:.3}", weighted_score(&values, &weights));
    println!("Interpretation: this is a structured comparison aid, not final judgment.");
}
