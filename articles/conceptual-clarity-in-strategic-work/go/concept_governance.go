// Concept-governance utility scaffold.
// Run: go run concept_governance.go

package main

import "fmt"

type Concept struct {
	ID                    string
	DefinitionClarity     float64
	BoundaryClarity       float64
	DistinctionQuality    float64
	OperationalImplication float64
	MeasurementValidity   float64
	RevisionCapacity      float64
	StakeholderVisibility float64
	EthicalVisibility     float64
	GovernanceMaturity    float64
}

func ClarityScore(c Concept) float64 {
	return 0.17*c.DefinitionClarity +
		0.14*c.BoundaryClarity +
		0.14*c.DistinctionQuality +
		0.13*c.OperationalImplication +
		0.15*c.MeasurementValidity +
		0.10*c.RevisionCapacity +
		0.07*c.StakeholderVisibility +
		0.06*c.EthicalVisibility +
		0.04*c.GovernanceMaturity
}

func Diagnosis(c Concept) string {
	if c.DefinitionClarity < 0.45 && c.MeasurementValidity < 0.45 {
		return "high_false_precision_risk"
	}
	if c.BoundaryClarity < 0.40 {
		return "concept_expansion_or_boundary_risk"
	}
	if c.RevisionCapacity < 0.35 {
		return "conceptual_drift_risk"
	}
	if ClarityScore(c) >= 0.64 {
		return "usable_for_strategy"
	}
	return "requires_clarity_review"
}

func main() {
	concepts := []Concept{
		{"CC001", 0.42, 0.31, 0.44, 0.52, 0.36, 0.29, 0.46, 0.41, 0.30},
		{"CC003", 0.64, 0.55, 0.68, 0.70, 0.60, 0.52, 0.66, 0.71, 0.50},
		{"CC005", 0.35, 0.28, 0.33, 0.40, 0.30, 0.27, 0.43, 0.39, 0.25},
	}

	for _, concept := range concepts {
		fmt.Printf("%s | %.3f | %s\n", concept.ID, ClarityScore(concept), Diagnosis(concept))
	}
}
