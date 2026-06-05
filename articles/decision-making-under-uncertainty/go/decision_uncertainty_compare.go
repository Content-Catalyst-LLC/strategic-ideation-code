// Decision-making under uncertainty comparison utility scaffold.
// Run: go run decision_uncertainty_compare.go

package main

import "fmt"

type OptionProfile struct {
	Name               string
	ExpectedReturn     float64
	Robustness         float64
	Flexibility        float64
	InformationQuality float64
	Exposure           float64
	OptionValue        float64
	Reversibility      float64
	EthicalResilience  float64
	LearningValue      float64
}

func DecisionProfile(o OptionProfile) float64 {
	return 0.14*o.ExpectedReturn +
		0.18*o.Robustness +
		0.16*o.Flexibility +
		0.12*o.InformationQuality -
		0.16*o.Exposure +
		0.14*o.OptionValue +
		0.10*o.Reversibility +
		0.10*o.EthicalResilience +
		0.10*o.LearningValue
}

func FragilityRisk(o OptionProfile) float64 {
	return 0.24*o.Exposure +
		0.18*(1-o.Robustness) +
		0.14*(1-o.Flexibility) +
		0.13*(1-o.OptionValue) +
		0.12*(1-o.Reversibility) +
		0.10*(1-o.EthicalResilience) +
		0.09*(1-o.InformationQuality)
}

func main() {
	options := []OptionProfile{
		{"High-Return Brittle Option", 0.86, 0.28, 0.31, 0.63, 0.82, 0.26, 0.22, 0.38, 0.30},
		{"Balanced Robust Option", 0.72, 0.79, 0.74, 0.72, 0.44, 0.72, 0.68, 0.68, 0.70},
		{"Exploratory Optionality Option", 0.61, 0.71, 0.88, 0.49, 0.53, 0.86, 0.82, 0.62, 0.88},
	}

	for _, option := range options {
		fmt.Printf("%s | profile %.3f | fragility %.3f\n",
			option.Name, DecisionProfile(option), FragilityRisk(option))
	}
}
