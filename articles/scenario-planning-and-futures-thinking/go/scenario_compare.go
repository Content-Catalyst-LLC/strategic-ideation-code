// Scenario comparison utility scaffold.
// Run: go run scenario_compare.go

package main

import (
	"fmt"
	"math"
)

type Strategy struct {
	Name                    string
	ScenarioValues          []float64
	Flexibility             float64
	ImplementationReadiness float64
	EthicalResilience       float64
	OptionValue             float64
}

func Mean(values []float64) float64 {
	sum := 0.0
	for _, v := range values {
		sum += v
	}
	return sum / float64(len(values))
}

func Worst(values []float64) float64 {
	worst := 1.0
	for _, v := range values {
		if v < worst {
			worst = v
		}
	}
	return worst
}

func StdDev(values []float64) float64 {
	mean := Mean(values)
	sum := 0.0
	for _, v := range values {
		sum += math.Pow(v-mean, 2)
	}
	return math.Sqrt(sum / float64(len(values)))
}

func RobustnessProfile(s Strategy) float64 {
	return 0.30*Worst(s.ScenarioValues) +
		0.24*Mean(s.ScenarioValues) +
		0.16*s.Flexibility +
		0.12*s.ImplementationReadiness +
		0.10*s.EthicalResilience +
		0.10*s.OptionValue -
		0.12*StdDev(s.ScenarioValues)
}

func main() {
	strategies := []Strategy{
		{"Short-Term Optimization Strategy", []float64{0.84, 0.41, 0.36, 0.48, 0.38}, 0.28, 0.86, 0.42, 0.30},
		{"Balanced Adaptive Strategy", []float64{0.74, 0.71, 0.67, 0.70, 0.66}, 0.73, 0.74, 0.68, 0.72},
		{"Resilience-Oriented Strategy", []float64{0.68, 0.75, 0.79, 0.73, 0.76}, 0.82, 0.66, 0.76, 0.78},
	}

	for _, s := range strategies {
		fmt.Printf("%s | mean %.3f | worst %.3f | robustness %.3f\n",
			s.Name, Mean(s.ScenarioValues), Worst(s.ScenarioValues), RobustnessProfile(s))
	}
}
