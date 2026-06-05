// Participation-quality evaluation utility scaffold.
// Run: go run codesign_compare.go

package main

import "fmt"

type ParticipationSystem struct {
	ID                   string
	Representation       float64
	Influence            float64
	Accessibility        float64
	Reciprocity          float64
	PowerAwareness       float64
	KnowledgeIntegration float64
	DecisionLinkage      float64
	Accountability       float64
	LearningMemory       float64
}

func ParticipationQuality(s ParticipationSystem) float64 {
	return 0.13*s.Representation +
		0.15*s.Influence +
		0.11*s.Accessibility +
		0.11*s.Reciprocity +
		0.13*s.PowerAwareness +
		0.12*s.KnowledgeIntegration +
		0.11*s.DecisionLinkage +
		0.10*s.Accountability +
		0.04*s.LearningMemory
}

func TokenismRisk(s ParticipationSystem) float64 {
	return 0.16*(1-s.Influence) +
		0.14*(1-s.DecisionLinkage) +
		0.14*(1-s.Accountability) +
		0.13*(1-s.Reciprocity) +
		0.13*(1-s.PowerAwareness) +
		0.11*(1-s.Representation) +
		0.10*(1-s.Accessibility) +
		0.09*(1-s.LearningMemory)
}

func Recommendation(s ParticipationSystem) string {
	if ParticipationQuality(s) >= 0.72 {
		return "strong_participatory_codesign_system"
	}
	if TokenismRisk(s) >= 0.68 {
		return "high_tokenism_or_extractive_participation_risk"
	}
	if s.Influence < 0.36 {
		return "participation_has_low_decision_influence"
	}
	return "developing_participatory_capability"
}

func main() {
	systems := []ParticipationSystem{
		{"P001", 0.34, 0.22, 0.40, 0.24, 0.28, 0.42, 0.20, 0.18, 0.24},
		{"P004", 0.86, 0.84, 0.82, 0.80, 0.86, 0.84, 0.82, 0.86, 0.84},
		{"P008", 0.58, 0.24, 0.52, 0.18, 0.30, 0.54, 0.22, 0.16, 0.20},
	}

	for _, s := range systems {
		fmt.Printf("%s | quality %.3f | tokenism risk %.3f | %s\n",
			s.ID,
			ParticipationQuality(s),
			TokenismRisk(s),
			Recommendation(s))
	}
}
