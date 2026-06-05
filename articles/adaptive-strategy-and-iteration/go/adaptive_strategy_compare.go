// Adaptive capability evaluation utility scaffold.
// Run: go run adaptive_strategy_compare.go

package main

import "fmt"

type Strategy struct {
	ID                    string
	Flexibility           float64
	LearningCapacity      float64
	Exploration           float64
	ExploitationBalance   float64
	Coherence             float64
	FeedbackIntelligence  float64
	Governance            float64
	SystemsAwareness      float64
	LearningMemory        float64
}

func AdaptiveScore(s Strategy) float64 {
	return 0.13*s.Flexibility +
		0.15*s.LearningCapacity +
		0.09*s.Exploration +
		0.11*s.ExploitationBalance +
		0.15*s.Coherence +
		0.13*s.FeedbackIntelligence +
		0.10*s.Governance +
		0.08*s.SystemsAwareness +
		0.06*s.LearningMemory
}

func OverAdaptationRisk(s Strategy) float64 {
	return 0.20*s.Flexibility*(1-s.Coherence) +
		0.18*(1-s.Governance) +
		0.16*(1-s.FeedbackIntelligence) +
		0.14*(1-s.LearningCapacity) +
		0.12*(1-s.ExploitationBalance) +
		0.10*(1-s.LearningMemory) +
		0.10*(1-s.SystemsAwareness)
}

func Recommendation(s Strategy) string {
	if AdaptiveScore(s) >= 0.74 {
		return "strong_adaptive_strategy_system"
	}
	if OverAdaptationRisk(s) >= 0.60 {
		return "high_over_adaptation_or_reactivity_risk"
	}
	if s.Coherence < 0.45 {
		return "strategic_drift_risk"
	}
	return "developing_adaptive_capability"
}

func main() {
	strategies := []Strategy{
		{"AS001", 0.24, 0.31, 0.18, 0.74, 0.81, 0.34, 0.62, 0.38, 0.36},
		{"AS002", 0.82, 0.84, 0.68, 0.79, 0.76, 0.82, 0.78, 0.74, 0.76},
		{"AS004", 0.86, 0.49, 0.57, 0.32, 0.28, 0.42, 0.24, 0.36, 0.30},
	}

	for _, s := range strategies {
		fmt.Printf("%s | adaptive score %.3f | over-adaptation risk %.3f | %s\n",
			s.ID,
			AdaptiveScore(s),
			OverAdaptationRisk(s),
			Recommendation(s))
	}
}
