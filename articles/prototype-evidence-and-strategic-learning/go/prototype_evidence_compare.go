// Prototype learning evaluation utility scaffold.
// Run: go run prototype_evidence_compare.go

package main

import "fmt"

type PrototypeSystem struct {
	ID                  string
	AssumptionClarity   float64
	LearningTargetFit   float64
	EvidenceQuality     float64
	BehavioralGrounding float64
	ContextRealism      float64
	SystemsAwareness    float64
	DecisionLinkage     float64
	EthicalReview       float64
	LearningMemory      float64
}

func LearningQuality(s PrototypeSystem) float64 {
	return 0.13*s.AssumptionClarity +
		0.13*s.LearningTargetFit +
		0.15*s.EvidenceQuality +
		0.13*s.BehavioralGrounding +
		0.11*s.ContextRealism +
		0.11*s.SystemsAwareness +
		0.11*s.DecisionLinkage +
		0.07*s.EthicalReview +
		0.06*s.LearningMemory
}

func ValidationTheaterRisk(s PrototypeSystem) float64 {
	return 0.17*(1-s.AssumptionClarity) +
		0.16*(1-s.EvidenceQuality) +
		0.14*(1-s.BehavioralGrounding) +
		0.13*(1-s.DecisionLinkage) +
		0.12*(1-s.LearningMemory) +
		0.11*(1-s.SystemsAwareness) +
		0.09*(1-s.EthicalReview) +
		0.08*(1-s.ContextRealism)
}

func Recommendation(s PrototypeSystem) string {
	if LearningQuality(s) >= 0.72 {
		return "strong_prototype_learning_system"
	}
	if ValidationTheaterRisk(s) >= 0.68 {
		return "high_validation_theater_risk"
	}
	if s.BehavioralGrounding < 0.36 {
		return "evidence_lacks_behavioral_grounding"
	}
	return "developing_prototype_learning_capability"
}

func main() {
	systems := []PrototypeSystem{
		{"PE001", 0.30, 0.28, 0.26, 0.22, 0.34, 0.24, 0.20, 0.28, 0.22},
		{"PE004", 0.84, 0.82, 0.84, 0.76, 0.80, 0.88, 0.82, 0.72, 0.82},
		{"PE007", 0.52, 0.46, 0.40, 0.26, 0.32, 0.30, 0.38, 0.36, 0.34},
	}

	for _, s := range systems {
		fmt.Printf("%s | learning quality %.3f | validation theater risk %.3f | %s\n",
			s.ID,
			LearningQuality(s),
			ValidationTheaterRisk(s),
			Recommendation(s))
	}
}
