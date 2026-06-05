// Strategic communication coherence comparison utility scaffold.
// Run: go run communication_coherence_compare.go

package main

import "fmt"

type Profile struct {
	Name           string
	Concept        float64
	Narrative      float64
	Evidence       float64
	Audience       float64
	Decision       float64
	Implementation float64
	Feedback       float64
	Governance     float64
	Ethics         float64
}

func Score(p Profile) float64 {
	return 0.12*p.Concept + 0.12*p.Narrative + 0.13*p.Evidence + 0.10*p.Audience +
		0.14*p.Decision + 0.12*p.Implementation + 0.08*p.Feedback +
		0.10*p.Governance + 0.09*p.Ethics
}

func main() {
	profiles := []Profile{
		{"Executive Strategy Briefing", 0.74, 0.76, 0.72, 0.70, 0.82, 0.62, 0.58, 0.70, 0.64},
		{"Stakeholder Explanation", 0.68, 0.74, 0.70, 0.82, 0.66, 0.60, 0.78, 0.66, 0.84},
		{"AI-Assisted Message Set", 0.52, 0.58, 0.46, 0.60, 0.48, 0.46, 0.44, 0.42, 0.40},
	}

	for _, p := range profiles {
		score := Score(p)
		fmt.Printf("%s | coherence strength %.3f | meaning loss risk %.3f\n", p.Name, score, 1-score)
	}
}
