// Strategic coherence comparison utility scaffold.
// Run: go run coherence_compare.go

package main

import "fmt"

type Context struct {
	Name           string
	Purpose        float64
	Priority       float64
	Tradeoff       float64
	Resources      float64
	Incentives     float64
	Interpretation float64
	Governance     float64
	Feedback       float64
	Memory         float64
	Ethics         float64
}

func Score(c Context) float64 {
	return 0.15*c.Purpose + 0.12*c.Priority + 0.11*c.Tradeoff + 0.13*c.Resources +
		0.13*c.Incentives + 0.11*c.Interpretation + 0.12*c.Governance +
		0.08*c.Feedback + 0.07*c.Memory + 0.08*c.Ethics
}

func main() {
	contexts := []Context{
		{"Symbolically Aligned Organization", 0.64, 0.50, 0.46, 0.46, 0.42, 0.50, 0.44, 0.48, 0.40, 0.54},
		{"Coherent Adaptive Organization", 0.84, 0.80, 0.78, 0.78, 0.80, 0.82, 0.78, 0.84, 0.76, 0.80},
		{"Metric-Substituted Organization", 0.68, 0.60, 0.54, 0.62, 0.36, 0.58, 0.52, 0.44, 0.50, 0.46},
	}

	for _, c := range contexts {
		score := Score(c)
		fmt.Printf("%s | coherence %.3f | drift risk %.3f\n", c.Name, score, 1-score)
	}
}
