// Strategic bad-idea risk comparison utility scaffold.
// Run: go run bad_idea_risk_compare.go

package main

import "fmt"

type BadIdea struct {
	Name           string
	Frame          float64
	Mechanism      float64
	Evidence       float64
	Implementation float64
	Incentive      float64
	Ethics         float64
	Support        float64
	Merit          float64
	Learning       float64
}

func Risk(i BadIdea) float64 {
	distortion := i.Support - i.Merit
	if distortion < 0 {
		distortion = 0
	}
	return 0.14*(1-i.Frame) + 0.12*(1-i.Mechanism) + 0.15*(1-i.Evidence) +
		0.14*(1-i.Implementation) + 0.12*(1-i.Incentive) + 0.12*(1-i.Ethics) +
		0.11*(1-i.Learning) + 0.10*distortion
}

func main() {
	ideas := []BadIdea{
		{"AI-Assisted Workflow Redesign", 0.54, 0.56, 0.52, 0.48, 0.44, 0.46, 0.78, 0.58, 0.46},
		{"Cost Consolidation Plan", 0.50, 0.52, 0.48, 0.44, 0.36, 0.38, 0.82, 0.54, 0.40},
		{"Reversible Pilot Portfolio", 0.74, 0.72, 0.70, 0.72, 0.68, 0.70, 0.58, 0.78, 0.82},
	}

	for _, i := range ideas {
		fmt.Printf("%s | bad-idea risk %.3f\n", i.Name, Risk(i))
	}
}
