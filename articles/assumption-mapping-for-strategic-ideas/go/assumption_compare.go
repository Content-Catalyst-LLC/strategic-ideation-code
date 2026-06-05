// Assumption prioritization utility scaffold.
// Run: go run assumption_compare.go

package main

import "fmt"

type Assumption struct {
	ID                       string
	Criticality              float64
	Uncertainty              float64
	EvidenceStrength         float64
	EvidenceRelevance        float64
	EvidenceTransferability  float64
	Testability              float64
	StakeholderSensitivity   float64
	SystemSensitivity        float64
}

func EvidenceComposite(a Assumption) float64 {
	return 0.40*a.EvidenceStrength + 0.30*a.EvidenceRelevance + 0.30*a.EvidenceTransferability
}

func EvidenceAdjustedRisk(a Assumption) float64 {
	return a.Criticality * a.Uncertainty * (1 - EvidenceComposite(a))
}

func LearningValue(a Assumption) float64 {
	return 0.34*EvidenceAdjustedRisk(a) +
		0.24*a.Testability +
		0.18*a.StakeholderSensitivity +
		0.14*a.SystemSensitivity +
		0.10*a.Criticality
}

func Recommendation(a Assumption) string {
	if EvidenceAdjustedRisk(a) >= 0.28 && a.Testability >= 0.65 {
		return "test_first"
	}
	if EvidenceAdjustedRisk(a) >= 0.28 {
		return "reduce_commitment_before_testing"
	}
	if a.StakeholderSensitivity >= 0.85 {
		return "stakeholder_review_required"
	}
	return "monitor"
}

func main() {
	assumptions := []Assumption{
		{"A001", 0.86, 0.70, 0.38, 0.62, 0.54, 0.78, 0.72, 0.70},
		{"A004", 0.90, 0.72, 0.34, 0.72, 0.60, 0.74, 0.94, 0.76},
		{"A015", 0.86, 0.66, 0.38, 0.62, 0.52, 0.62, 0.70, 0.74},
	}

	for _, a := range assumptions {
		fmt.Printf("%s | risk %.3f | learning %.3f | %s\n",
			a.ID,
			EvidenceAdjustedRisk(a),
			LearningValue(a),
			Recommendation(a))
	}
}
