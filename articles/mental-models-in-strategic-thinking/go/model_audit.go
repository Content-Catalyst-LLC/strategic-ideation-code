// Model-audit utility scaffold.
// Run: go run model_audit.go

package main

import "fmt"

type ModelProfile struct {
	ID                     string
	SystemsRichness        float64
	ProbabilisticDepth     float64
	ModelFlexibility       float64
	ModelPlurality         float64
	RevisionCapacity       float64
	InstitutionalEmbedding float64
	EthicalVisibility      float64
	StakeholderVisibility  float64
	EvidenceResponsiveness float64
}

func AdaptiveScore(m ModelProfile) float64 {
	return 0.17*m.SystemsRichness +
		0.13*m.ProbabilisticDepth +
		0.16*m.ModelFlexibility +
		0.14*m.ModelPlurality +
		0.16*m.RevisionCapacity -
		0.08*m.InstitutionalEmbedding +
		0.12*m.EthicalVisibility +
		0.10*m.StakeholderVisibility +
		0.10*m.EvidenceResponsiveness
}

func MonocultureRisk(m ModelProfile) float64 {
	return 0.28*m.InstitutionalEmbedding +
		0.20*(1-m.ModelPlurality) +
		0.18*(1-m.ModelFlexibility) +
		0.18*(1-m.RevisionCapacity) +
		0.16*(1-m.StakeholderVisibility)
}

func Diagnosis(m ModelProfile) string {
	if AdaptiveScore(m) >= 0.75 && MonocultureRisk(m) < 0.35 {
		return "adaptive_model_strength"
	}
	if MonocultureRisk(m) >= 0.65 {
		return "model_monoculture_or_lock_in_risk"
	}
	if m.EthicalVisibility < 0.45 || m.StakeholderVisibility < 0.45 {
		return "ethical_or_stakeholder_blind_spot"
	}
	return "requires_model_review"
}

func main() {
	models := []ModelProfile{
		{"M001", 0.24, 0.21, 0.19, 0.22, 0.22, 0.58, 0.31, 0.28, 0.34},
		{"M003", 0.89, 0.84, 0.88, 0.86, 0.87, 0.71, 0.82, 0.80, 0.86},
		{"M004", 0.33, 0.29, 0.18, 0.24, 0.16, 0.91, 0.42, 0.39, 0.27},
	}

	for _, model := range models {
		fmt.Printf("%s | adaptive %.3f | risk %.3f | %s\n", model.ID, AdaptiveScore(model), MonocultureRisk(model), Diagnosis(model))
	}
}
