// Search-breadth review utility scaffold.
// Run: go run search_breadth.go

package main

import "fmt"

type Idea struct {
	ID                    string
	StakeholderVisibility float64
	NoveltyLevel          float64
	EvidencePathway       float64
	StrategicRelevance    float64
	ImplementationPathway float64
	SearchBreadth         float64
	ClosurePressure       float64
	AssumptionBurden      float64
}

func SearchBreadthScore(i Idea) float64 {
	return 0.12*i.StakeholderVisibility +
		0.12*i.NoveltyLevel +
		0.12*i.EvidencePathway +
		0.14*i.StrategicRelevance +
		0.10*i.ImplementationPathway +
		0.16*i.SearchBreadth -
		0.12*i.ClosurePressure -
		0.08*i.AssumptionBurden
}

func Recommendation(i Idea) string {
	if i.ClosurePressure >= 0.80 {
		return "premature_closure_check"
	}
	if i.SearchBreadth < 0.35 {
		return "expand_search_before_evaluation"
	}
	if i.StakeholderVisibility < 0.40 {
		return "add_stakeholder_visibility_review"
	}
	if SearchBreadthScore(i) >= 0.45 {
		return "strong_search_breadth_contributor"
	}
	return "revise_or_defer"
}

func main() {
	ideas := []Idea{
		{"I001", 0.28, 0.26, 0.40, 0.44, 0.74, 0.24, 0.80, 0.36},
		{"I007", 0.76, 0.84, 0.72, 0.82, 0.64, 0.86, 0.28, 0.52},
		{"I013", 0.74, 0.72, 0.76, 0.86, 0.66, 0.78, 0.30, 0.40},
	}

	for _, idea := range ideas {
		fmt.Printf("%s | %.3f | %s\n", idea.ID, SearchBreadthScore(idea), Recommendation(idea))
	}
}
