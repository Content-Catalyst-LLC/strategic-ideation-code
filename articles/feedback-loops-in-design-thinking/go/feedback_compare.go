// Feedback-loop evaluation utility scaffold.
// Run: go run feedback_compare.go

package main

import "fmt"

type FeedbackSystem struct {
	ID                     string
	SignalQuality          float64
	InterpretationCapacity float64
	AdjustmentSpeed        float64
	UserInsightDepth       float64
	Stability              float64
	EthicalIntegrity       float64
	SystemsAwareness       float64
	DecisionLinkage        float64
	LearningMemory         float64
}

func FeedbackProfile(s FeedbackSystem) float64 {
	return 0.13*s.SignalQuality +
		0.13*s.InterpretationCapacity +
		0.10*s.AdjustmentSpeed +
		0.13*s.UserInsightDepth +
		0.10*s.Stability +
		0.11*s.EthicalIntegrity +
		0.10*s.SystemsAwareness +
		0.10*s.DecisionLinkage +
		0.10*s.LearningMemory
}

func NoisyChurnRisk(s FeedbackSystem) float64 {
	return 0.16*s.AdjustmentSpeed +
		0.15*(1-s.SignalQuality) +
		0.15*(1-s.InterpretationCapacity) +
		0.13*(1-s.Stability) +
		0.12*(1-s.SystemsAwareness) +
		0.12*(1-s.EthicalIntegrity) +
		0.10*(1-s.DecisionLinkage) +
		0.07*(1-s.LearningMemory)
}

func Recommendation(s FeedbackSystem) string {
	if FeedbackProfile(s) >= 0.68 {
		return "strong_feedback_learning_system"
	}
	if NoisyChurnRisk(s) >= 0.64 {
		return "high_noisy_churn_or_feedback_theater_risk"
	}
	if s.DecisionLinkage < 0.40 {
		return "feedback_not_linked_to_decisions"
	}
	return "developing_feedback_capability"
}

func main() {
	systems := []FeedbackSystem{
		{"F001", 0.34, 0.31, 0.29, 0.36, 0.41, 0.38, 0.32, 0.28, 0.26},
		{"F004", 0.82, 0.84, 0.63, 0.88, 0.72, 0.72, 0.84, 0.80, 0.82},
		{"F006", 0.62, 0.42, 0.34, 0.46, 0.50, 0.40, 0.38, 0.24, 0.28},
	}

	for _, s := range systems {
		fmt.Printf("%s | profile %.3f | noisy churn risk %.3f | %s\n",
			s.ID,
			FeedbackProfile(s),
			NoisyChurnRisk(s),
			Recommendation(s))
	}
}
