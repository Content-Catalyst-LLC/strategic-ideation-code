// Advanced option-evaluation utility scaffold.
// Run: go run option_evaluation.go

package main

import "fmt"

type Option struct {
	ID                   string
	Reversibility        float64
	DependencyComplexity float64
	PortfolioFit         float64
	ScenarioRobustness   float64
	SequencingValue      float64
	CommitmentLevel      string
}

func ArchitectureScore(o Option) float64 {
	return 0.16*o.Reversibility -
		0.10*o.DependencyComplexity +
		0.24*o.PortfolioFit +
		0.24*o.ScenarioRobustness +
		0.22*o.SequencingValue
}

func ArchitectureFlag(o Option) string {
	score := ArchitectureScore(o)
	if o.CommitmentLevel == "high" && o.Reversibility < 0.50 {
		return "high_commitment_low_reversibility"
	}
	if o.DependencyComplexity > 0.60 {
		return "dependency_complexity_review"
	}
	if score >= 0.75 {
		return "strong_option_architecture"
	}
	return "needs_architecture_refinement"
}

func main() {
	options := []Option{
		{"O001", 0.72, 0.41, 0.92, 0.78, 0.86, "medium"},
		{"O005", 0.43, 0.67, 0.84, 0.72, 0.75, "high"},
		{"O010", 0.70, 0.42, 0.91, 0.84, 0.90, "medium"},
	}

	for _, option := range options {
		fmt.Printf("%s | %.3f | %s\n", option.ID, ArchitectureScore(option), ArchitectureFlag(option))
	}
}
