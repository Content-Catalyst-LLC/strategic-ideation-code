// Prototype and experiment evaluation utility scaffold.
// Run: go run experiment_compare.go

package main

import "fmt"

type System struct {
	ID                    string
	Speed                 float64
	CostEfficiency        float64
	InsightDepth          float64
	UserValidation        float64
	AssumptionCriticality float64
	EvidenceQuality       float64
	SystemsAwareness      float64
	EthicalReview         float64
	DecisionLinkage       float64
	LearningMemory        float64
}

func ExperimentationProfile(s System) float64 {
	return 0.10*s.Speed +
		0.09*s.CostEfficiency +
		0.15*s.InsightDepth +
		0.12*s.UserValidation +
		0.12*s.AssumptionCriticality +
		0.14*s.EvidenceQuality +
		0.10*s.SystemsAwareness +
		0.08*s.EthicalReview +
		0.10*s.DecisionLinkage +
		0.10*s.LearningMemory
}

func SuperficialTestingRisk(s System) float64 {
	return 0.14*s.Speed +
		0.16*(1-s.InsightDepth) +
		0.15*(1-s.EvidenceQuality) +
		0.13*(1-s.SystemsAwareness) +
		0.13*(1-s.EthicalReview) +
		0.13*(1-s.DecisionLinkage) +
		0.09*(1-s.AssumptionCriticality) +
		0.07*(1-s.LearningMemory)
}

func Recommendation(s System) string {
	if ExperimentationProfile(s) >= 0.66 {
		return "strong_experimentation_learning_system"
	}
	if SuperficialTestingRisk(s) >= 0.62 {
		return "high_superficial_testing_or_prototype_theater_risk"
	}
	if s.DecisionLinkage < 0.42 {
		return "learning_not_linked_to_decisions"
	}
	return "developing_experimentation_capability"
}

func main() {
	systems := []System{
		{"E001", 0.24, 0.31, 0.42, 0.36, 0.44, 0.38, 0.34, 0.42, 0.30, 0.32},
		{"E004", 0.61, 0.67, 0.89, 0.84, 0.86, 0.88, 0.82, 0.70, 0.82, 0.80},
		{"E006", 0.70, 0.50, 0.36, 0.42, 0.38, 0.34, 0.28, 0.30, 0.24, 0.22},
	}

	for _, s := range systems {
		fmt.Printf("%s | profile %.3f | superficial testing risk %.3f | %s\n",
			s.ID,
			ExperimentationProfile(s),
			SuperficialTestingRisk(s),
			Recommendation(s))
	}
}
