// Strategy-to-tactics alignment utility scaffold.
// Run: go run strategy_tactics_alignment.go

package main

import "fmt"

type Tactic struct {
	ID                  string
	AlignmentToStrategy float64
	ExecutionReadiness  float64
	ResourceFit         float64
	FeedbackCapture     float64
	LearningRouting     float64
	DeliveryRisk        float64
}

func TranslationScore(t Tactic) float64 {
	return 0.26*t.AlignmentToStrategy +
		0.20*t.ExecutionReadiness +
		0.16*t.ResourceFit +
		0.18*t.FeedbackCapture +
		0.20*t.LearningRouting -
		0.12*t.DeliveryRisk
}

func GapType(t Tactic) string {
	if t.AlignmentToStrategy < 0.65 {
		return "strategic_alignment_gap"
	}
	if t.ExecutionReadiness < 0.60 {
		return "execution_readiness_gap"
	}
	if t.LearningRouting < 0.65 {
		return "learning_routing_gap"
	}
	if t.DeliveryRisk > 0.40 {
		return "delivery_risk_gap"
	}
	return "acceptable_translation"
}

func main() {
	tactics := []Tactic{
		{"T003", 0.92, 0.69, 0.70, 0.74, 0.78, 0.28},
		{"T009", 0.78, 0.55, 0.57, 0.61, 0.59, 0.46},
		{"T013", 0.88, 0.57, 0.54, 0.86, 0.83, 0.41},
	}

	for _, tactic := range tactics {
		fmt.Printf("%s | %.3f | %s\n", tactic.ID, TranslationScore(tactic), GapType(tactic))
	}
}
