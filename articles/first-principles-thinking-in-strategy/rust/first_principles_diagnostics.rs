struct Context { id: &'static str, assumptions: f64, clarity: f64, constraints: f64, reconstruction: f64, adaptation: f64 }
fn score(c: &Context) -> f64 { -0.16*c.assumptions + 0.18*c.clarity + 0.18*c.constraints + 0.18*c.reconstruction + 0.14*c.adaptation }
fn main() {
    let contexts = vec![Context{id:"FP001",assumptions:0.84,clarity:0.31,constraints:0.28,reconstruction:0.34,adaptation:0.39}, Context{id:"FP003",assumptions:0.22,clarity:0.88,constraints:0.91,reconstruction:0.89,adaptation:0.92}];
    for c in contexts { println!("{} | {:.3}", c.id, score(&c)); }
}
