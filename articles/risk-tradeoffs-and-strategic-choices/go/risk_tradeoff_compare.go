// Strategic tradeoff comparison utility scaffold.
// Run: go run risk_tradeoff_compare.go

package main

import "fmt"

type OptionProfile struct {
	Name              string
	ShortTermReturn   float64
	Resilience        float64
	Flexibility       float64
	Legitimacy        float64
	OpportunityValue  float64
	Exposure          float64
	Reversibility     float64
	EthicalResilience float64
	LearningValue     float64
}

func TradeoffScore(o OptionProfile) float64 {
	return 0.18*o.ShortTermReturn +
		0.20*o.Resilience +
		0.16*o.Flexibility +
		0.14*o.Legitimacy +
		0.14*o.OpportunityValue -
		0.18*o.Exposure +
		0.08*o.Reversibility +
		0.08*o.EthicalResilience +
		0.08*o.LearningValue
}

func FragilityWarning(o OptionProfile) float64 {
	return 0.26*o.Exposure +
		0.18*(1-o.Resilience) +
		0.14*(1-o.Flexibility) +
		0.12*(1-o.Legitimacy) +
		0.12*(1-o.OpportunityValue) +
		0.10*(1-o.Reversibility) +
		0.08*(1-o.EthicalResilience)
}

func main() {
	options := []OptionProfile{
		{"Efficiency-Optimized Option", 0.86, 0.32, 0.36, 0.48, 0.34, 0.74, 0.30, 0.42, 0.34},
		{"Balanced Strategic Option", 0.71, 0.74, 0.76, 0.72, 0.70, 0.46, 0.68, 0.70, 0.72},
		{"Resilience-First Option", 0.58, 0.88, 0.79, 0.81, 0.76, 0.34, 0.72, 0.82, 0.70},
	}

	for _, option := range options {
		fmt.Printf("%s | tradeoff score %.3f | fragility warning %.3f\n",
			option.Name, TradeoffScore(option), FragilityWarning(option))
	}
}
