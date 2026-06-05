// Strategic foresight comparison utility scaffold.
// Run: go run foresight_compare.go

package main

import "fmt"

type Strategy struct {
	Name                string
	ShortTermReturn     float64
	ForesightDepth      float64
	Resilience          float64
	Flexibility         float64
	PathDependenceRisk  float64
	SignalCapacity      float64
	ScenarioCapacity    float64
	OptionValue         float64
	EthicsReview        float64
	GovernanceCapacity  float64
}

func FutureViability(s Strategy) float64 {
	return 0.18*s.ForesightDepth +
		0.18*s.Resilience +
		0.16*s.Flexibility +
		0.14*s.OptionValue +
		0.12*s.ScenarioCapacity +
		0.10*s.SignalCapacity +
		0.08*s.GovernanceCapacity +
		0.08*s.EthicsReview -
		0.14*s.PathDependenceRisk
}

func ShortTermBias(s Strategy) float64 {
	return s.ShortTermReturn - ((s.ForesightDepth + s.Resilience + s.Flexibility + s.OptionValue) / 4.0)
}

func Recommendation(s Strategy) string {
	if FutureViability(s) >= 0.70 {
		return "strong_long_term_foresight_profile"
	}
	if ShortTermBias(s) >= 0.35 {
		return "short_term_optimization_risk"
	}
	if s.PathDependenceRisk >= 0.72 {
		return "high_path_dependence_and_lock_in_risk"
	}
	return "developing_foresight_capability"
}

func main() {
	strategies := []Strategy{
		{"Short-Term Efficiency Strategy", 0.86, 0.24, 0.32, 0.28, 0.71, 0.30, 0.26, 0.30, 0.34, 0.42},
		{"Balanced Foresight Strategy", 0.72, 0.79, 0.76, 0.74, 0.39, 0.76, 0.74, 0.72, 0.68, 0.74},
		{"Resilience-Biased Long-Horizon Strategy", 0.61, 0.84, 0.88, 0.79, 0.34, 0.80, 0.82, 0.78, 0.76, 0.80},
	}

	for _, s := range strategies {
		fmt.Printf("%s | future viability %.3f | short-term bias %.3f | %s\n",
			s.Name, FutureViability(s), ShortTermBias(s), Recommendation(s))
	}
}
