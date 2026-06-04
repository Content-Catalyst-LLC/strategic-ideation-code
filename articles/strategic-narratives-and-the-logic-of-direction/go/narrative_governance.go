// Narrative-governance utility scaffold.
// Run: go run narrative_governance.go

package main

import "fmt"

type Narrative struct {
	ID                    string
	DiagnosisClarity      float64
	PurposeClarity        float64
	ChoiceClarity         float64
	SequencingLogic       float64
	RoleClarity           float64
	FutureCredibility     float64
	AccountabilityStrength float64
	EvidenceGrounding     float64
	StakeholderVisibility float64
	EthicalVisibility     float64
}

func CoherenceScore(n Narrative) float64 {
	return 0.14*n.DiagnosisClarity +
		0.12*n.PurposeClarity +
		0.14*n.ChoiceClarity +
		0.12*n.SequencingLogic +
		0.11*n.RoleClarity +
		0.10*n.FutureCredibility +
		0.11*n.AccountabilityStrength +
		0.08*n.EvidenceGrounding +
		0.05*n.StakeholderVisibility +
		0.03*n.EthicalVisibility
}

func Diagnosis(n Narrative) string {
	if n.ChoiceClarity < 0.40 {
		return "weak_choice_logic"
	}
	if n.SequencingLogic < 0.40 {
		return "weak_pathway_logic"
	}
	if n.AccountabilityStrength < 0.40 {
		return "narrative_performance_gap_risk"
	}
	if CoherenceScore(n) >= 0.72 {
		return "strong_directional_narrative"
	}
	return "requires_narrative_review"
}

func main() {
	narratives := []Narrative{
		{"SN001", 0.32, 0.44, 0.28, 0.30, 0.36, 0.42, 0.25, 0.34, 0.38, 0.35},
		{"SN003", 0.86, 0.82, 0.76, 0.84, 0.78, 0.80, 0.82, 0.84, 0.78, 0.81},
		{"SN004", 0.41, 0.48, 0.35, 0.33, 0.39, 0.45, 0.31, 0.40, 0.43, 0.39},
	}

	for _, narrative := range narratives {
		fmt.Printf("%s | %.3f | %s\n", narrative.ID, CoherenceScore(narrative), Diagnosis(narrative))
	}
}
