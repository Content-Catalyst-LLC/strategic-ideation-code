// Strategic future-ready ideation comparison utility scaffold.
// Run: go run future_ideation_compare.go

package main

import "fmt"

type FutureIdea struct {
	Name           string
	Frame          float64
	Evidence       float64
	Adaptability   float64
	Scenario       float64
	Stakeholder    float64
	Implementation float64
	Ethics         float64
	Learning       float64
	OptionValue    float64
	AI             float64
}

func FutureReadyScore(i FutureIdea) float64 {
	return 0.11*i.Frame + 0.11*i.Evidence + 0.11*i.Adaptability + 0.12*i.Scenario +
		0.11*i.Stakeholder + 0.10*i.Implementation + 0.11*i.Ethics + 0.12*i.Learning +
		0.07*i.OptionValue + 0.04*i.AI
}

func main() {
	ideas := []FutureIdea{
		{"Scenario-Linked Option Portfolio", 0.78, 0.72, 0.84, 0.86, 0.70, 0.70, 0.76, 0.86, 0.90, 0.62},
		{"Participatory Strategy Lab", 0.80, 0.74, 0.78, 0.72, 0.86, 0.64, 0.84, 0.78, 0.72, 0.56},
		{"Rapid Automation Initiative", 0.54, 0.52, 0.48, 0.46, 0.42, 0.50, 0.44, 0.42, 0.46, 0.38},
	}

	for _, i := range ideas {
		score := FutureReadyScore(i)
		fmt.Printf("%s | future-ready score %.3f | future risk %.3f\n", i.Name, score, 1-score)
	}
}
