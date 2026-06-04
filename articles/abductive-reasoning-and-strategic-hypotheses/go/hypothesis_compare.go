// Hypothesis-comparison utility scaffold.
// Run: go run hypothesis_compare.go

package main

import "fmt"

type Hypothesis struct {
	ID          string
	Explain    float64
	Test       float64
	Evidence   float64
	Relevance  float64
	Stakeholder float64
	Systems    float64
	Action     float64
	Risk       float64
	Reversible float64
}

func Score(h Hypothesis) float64 {
	return 0.16*h.Explain +
		0.14*h.Test +
		0.14*h.Evidence +
		0.16*h.Relevance +
		0.12*h.Stakeholder +
		0.12*h.Systems +
		0.10*h.Action +
		0.06*h.Reversible -
		0.10*h.Risk
}

func Recommendation(h Hypothesis) string {
	score := Score(h)
	if score >= 0.72 && h.Evidence >= 0.65 && h.Reversible >= 0.55 {
		return "prototype_or_pilot"
	}
	if score >= 0.64 {
		return "targeted_research_or_low_risk_test"
	}
	if score >= 0.54 {
		return "monitor_and_compare"
	}
	return "hold_reframe_or_archive"
}

func main() {
	hypotheses := []Hypothesis{
		{"H001", 0.82, 0.74, 0.68, 0.86, 0.72, 0.76, 0.72, 0.52, 0.74},
		{"H004", 0.84, 0.70, 0.66, 0.86, 0.92, 0.78, 0.64, 0.58, 0.66},
		{"H010", 0.88, 0.68, 0.72, 0.90, 0.66, 0.86, 0.62, 0.66, 0.58},
	}

	for _, h := range hypotheses {
		fmt.Printf("%s | %.3f | %s\n", h.ID, Score(h), Recommendation(h))
	}
}
