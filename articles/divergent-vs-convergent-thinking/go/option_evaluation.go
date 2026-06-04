// Option-evaluation utility scaffold.
// Run: go run option_evaluation.go

package main

import "fmt"

type Idea struct {
	ID                      string
	Novelty                 float64
	StrategicFit            float64
	EvidenceStrength        float64
	Feasibility             float64
	StakeholderValue        float64
	RiskVisibility          float64
	EthicalLegitimacy       float64
	ImplementationReadiness float64
	AssumptionBurden        float64
}

func IdeaScore(i Idea) float64 {
	return 0.12*i.Novelty +
		0.18*i.StrategicFit +
		0.14*i.EvidenceStrength +
		0.12*i.Feasibility +
		0.14*i.StakeholderValue +
		0.10*i.RiskVisibility +
		0.12*i.EthicalLegitimacy +
		0.10*i.ImplementationReadiness -
		0.08*i.AssumptionBurden
}

func Recommendation(i Idea) string {
	score := IdeaScore(i)
	if score >= 0.72 {
		return "advance_to_evidence_gate"
	}
	if i.StakeholderValue < 0.35 || i.EthicalLegitimacy < 0.35 {
		return "stakeholder_or_ethics_review_before_advancing"
	}
	if i.AssumptionBurden >= 0.60 {
		return "assumption_mapping_required"
	}
	if score >= 0.58 {
		return "revise_and_retest"
	}
	return "hold_or_reframe"
}

func main() {
	ideas := []Idea{
		{"I003", 0.74, 0.82, 0.70, 0.76, 0.72, 0.78, 0.76, 0.74, 0.38},
		{"I005", 0.82, 0.38, 0.24, 0.30, 0.46, 0.28, 0.42, 0.22, 0.76},
		{"I011", 0.72, 0.78, 0.66, 0.62, 0.92, 0.76, 0.90, 0.58, 0.40},
	}

	for _, idea := range ideas {
		fmt.Printf("%s | %.3f | %s\n", idea.ID, IdeaScore(idea), Recommendation(idea))
	}
}
