// Constraint-calibration utility scaffold.
// Run: go run constraint_calibration.go

package main

import "fmt"

type Context struct {
	ID                         string
	ResourcePressure           float64
	TechnicalRigidity          float64
	InstitutionalRigidity      float64
	EcologicalBoundaryPressure float64
	EthicalVisibility          float64
	SearchFocus               float64
	AdaptiveOpportunity        float64
	StakeholderLegitimacy      float64
	LearningCapacity           float64
	ImplementationReadiness    float64
}

func ProductiveProfile(c Context) float64 {
	return -0.10*c.ResourcePressure -
		0.10*c.TechnicalRigidity -
		0.10*c.InstitutionalRigidity +
		0.12*c.EcologicalBoundaryPressure +
		0.16*c.EthicalVisibility +
		0.16*c.SearchFocus +
		0.16*c.AdaptiveOpportunity +
		0.14*c.StakeholderLegitimacy +
		0.14*c.LearningCapacity +
		0.12*c.ImplementationReadiness
}

func RigidityRisk(c Context) float64 {
	rigidity := 0.24*c.ResourcePressure +
		0.25*c.TechnicalRigidity +
		0.27*c.InstitutionalRigidity +
		0.24*c.EcologicalBoundaryPressure
	return rigidity * (1 - c.LearningCapacity)
}

func DiffusionRisk(c Context) float64 {
	return (1 - c.SearchFocus) * c.AdaptiveOpportunity
}

func Diagnosis(c Context) string {
	if DiffusionRisk(c) >= 0.42 {
		return "under_constrained_diffusion_risk"
	}
	if RigidityRisk(c) >= 0.42 {
		return "over_constrained_rigidity_risk"
	}
	if c.StakeholderLegitimacy < 0.40 {
		return "stakeholder_legitimacy_gap"
	}
	if ProductiveProfile(c) >= 0.42 {
		return "productive_constraint_profile"
	}
	return "requires_constraint_review"
}

func main() {
	contexts := []Context{
		{"CC001", 0.12, 0.18, 0.16, 0.20, 0.38, 0.24, 0.38, 0.42, 0.36, 0.34},
		{"CC002", 0.54, 0.47, 0.43, 0.52, 0.66, 0.78, 0.81, 0.72, 0.78, 0.76},
		{"CC007", 0.66, 0.52, 0.57, 0.92, 0.88, 0.74, 0.70, 0.82, 0.76, 0.60},
	}

	for _, context := range contexts {
		fmt.Printf("%s | %.3f | rigidity %.3f | diffusion %.3f | %s\n",
			context.ID,
			ProductiveProfile(context),
			RigidityRisk(context),
			DiffusionRisk(context),
			Diagnosis(context))
	}
}
