// Leverage-point comparison utility scaffold.
// Run: go run leverage_compare.go

package main

import "fmt"

type LeveragePoint struct {
	ID                         string
	ImplementationEase         float64
	StructuralDepth            float64
	SystemSensitivity          float64
	FeedbackInfluence          float64
	InformationEffect          float64
	RulePower                  float64
	GoalAlignment              float64
	ParadigmRelevance          float64
	TransformativePotential    float64
	LegitimacyRequirement      float64
	UnintendedConsequenceRisk  float64
	LearningCapacity           float64
}

func LeverageScore(l LeveragePoint) float64 {
	return 0.06*l.ImplementationEase +
		0.16*l.StructuralDepth +
		0.14*l.SystemSensitivity +
		0.13*l.FeedbackInfluence +
		0.11*l.InformationEffect +
		0.13*l.RulePower +
		0.13*l.GoalAlignment +
		0.08*l.ParadigmRelevance +
		0.14*l.TransformativePotential +
		0.08*l.LearningCapacity -
		0.06*l.UnintendedConsequenceRisk
}

func GovernanceNeed(l LeveragePoint) float64 {
	return 0.26*l.LegitimacyRequirement +
		0.24*l.UnintendedConsequenceRisk +
		0.22*l.TransformativePotential +
		0.14*(1-l.ImplementationEase) +
		0.14*l.ParadigmRelevance
}

func Recommendation(l LeveragePoint) string {
	if LeverageScore(l) >= 0.72 && GovernanceNeed(l) >= 0.68 {
		return "high_leverage_high_governance_need"
	}
	if LeverageScore(l) >= 0.68 {
		return "high_leverage_candidate"
	}
	if l.ImplementationEase >= 0.70 && l.StructuralDepth <= 0.45 {
		return "easy_but_shallow"
	}
	return "moderate_leverage_review"
}

func main() {
	points := []LeveragePoint{
		{"L001", 0.86, 0.22, 0.28, 0.28, 0.31, 0.20, 0.28, 0.16, 0.24, 0.24, 0.26, 0.34},
		{"L006", 0.44, 0.82, 0.82, 0.76, 0.66, 0.90, 0.78, 0.58, 0.82, 0.72, 0.70, 0.70},
		{"L008", 0.21, 0.96, 0.88, 0.82, 0.60, 0.78, 0.96, 0.98, 0.96, 0.90, 0.82, 0.78},
	}

	for _, point := range points {
		fmt.Printf("%s | %.3f | %.3f | %s\n",
			point.ID,
			LeverageScore(point),
			GovernanceNeed(point),
			Recommendation(point))
	}
}
