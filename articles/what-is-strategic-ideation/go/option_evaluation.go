// Go option-evaluation utility scaffold.
// Run: go run option_evaluation.go

package main

import "fmt"

type Option struct {
	ID              string
	StrategicFit    float64
	Feasibility     float64
	SystemsLeverage float64
	LearningValue   float64
	Uncertainty     float64
}

func Score(o Option) float64 {
	return 0.28*o.StrategicFit +
		0.18*o.Feasibility +
		0.24*o.SystemsLeverage +
		0.18*o.LearningValue -
		0.12*o.Uncertainty
}

func main() {
	options := []Option{
		{"I001", 0.91, 0.82, 0.74, 0.88, 0.24},
		{"I004", 0.78, 0.76, 0.65, 0.95, 0.28},
		{"I008", 0.86, 0.70, 0.89, 0.88, 0.37},
	}

	for _, option := range options {
		score := Score(option)
		fmt.Printf("%s | %.3f\n", option.ID, score)
	}
}
