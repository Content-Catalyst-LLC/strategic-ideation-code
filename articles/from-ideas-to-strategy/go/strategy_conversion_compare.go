// Strategic initiative conversion comparison utility scaffold.
// Run: go run strategy_conversion_compare.go

package main

import "fmt"

type Initiative struct {
	Name                  string
	Feasibility           float64
	Viability             float64
	Desirability          float64
	IntegrationDifficulty float64
	ExecutionReadiness    float64
	StrategicFit          float64
	EvidenceConfidence    float64
	EthicalResilience     float64
}

func ConversionScore(i Initiative) float64 {
	return 0.16*i.Feasibility +
		0.18*i.Viability +
		0.16*i.Desirability -
		0.12*i.IntegrationDifficulty +
		0.16*i.ExecutionReadiness +
		0.12*i.StrategicFit +
		0.08*i.EvidenceConfidence +
		0.06*i.EthicalResilience
}

func main() {
	initiatives := []Initiative{
		{"High-Idea Low-Execution Concept", 0.78, 0.38, 0.82, 0.72, 0.29, 0.62, 0.42, 0.54},
		{"Balanced Strategic Initiative", 0.74, 0.79, 0.77, 0.44, 0.81, 0.84, 0.76, 0.72},
		{"Integration-Challenged Initiative", 0.69, 0.71, 0.84, 0.83, 0.52, 0.76, 0.58, 0.60},
	}

	for _, i := range initiatives {
		score := ConversionScore(i)
		fmt.Printf("%s | score %.3f | confidence-adjusted %.3f\n", i.Name, score, score*i.EvidenceConfidence)
	}
}
