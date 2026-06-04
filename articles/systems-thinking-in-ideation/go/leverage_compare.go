// Leverage-point comparison utility scaffold.
// Run: go run leverage_compare.go

package main

import "fmt"

type LeveragePoint struct {
	ID          string
	Depth       float64
	Feasibility float64
	Evidence    float64
	Legitimacy  float64
	Reversible  float64
	Sensitivity float64
	Risk        float64
	Time        float64
}

func Score(l LeveragePoint) float64 {
	return 0.22*l.Depth +
		0.12*l.Feasibility +
		0.12*l.Evidence +
		0.12*l.Legitimacy +
		0.08*l.Reversible +
		0.16*l.Sensitivity -
		0.10*l.Risk -
		0.08*l.Time
}

func Recommendation(l LeveragePoint) string {
	if l.Depth >= 0.80 && l.Risk >= 0.60 {
		return "stage_high_leverage_intervention_with_guardrails"
	}
	if l.Legitimacy < 0.60 {
		return "add_stakeholder_legitimacy_review"
	}
	if Score(l) >= 0.55 {
		return "priority_leverage_candidate"
	}
	if l.Depth < 0.35 {
		return "low_leverage_surface_fix"
	}
	return "develop_or_compare"
}

func main() {
	points := []LeveragePoint{
		{"L001", 0.24, 0.82, 0.54, 0.34, 0.88, 0.28, 0.30, 0.22},
		{"L003", 0.82, 0.62, 0.68, 0.70, 0.58, 0.84, 0.54, 0.60},
		{"L007", 0.80, 0.70, 0.72, 0.68, 0.76, 0.82, 0.34, 0.46},
	}

	for _, p := range points {
		fmt.Printf("%s | %.3f | %s\n", p.ID, Score(p), Recommendation(p))
	}
}
