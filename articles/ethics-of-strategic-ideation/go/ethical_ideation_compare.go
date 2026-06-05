// Strategic ethical ideation comparison utility scaffold.
// Run: go run ethical_ideation_compare.go

package main

import "fmt"

type EthicalIdea struct {
	Name           string
	Voice          float64
	Evidence       float64
	Burden         float64
	Uncertainty    float64
	Reversibility  float64
	LongTerm       float64
	AI             float64
	Accountability float64
	Redress        float64
}

func Legitimacy(i EthicalIdea) float64 {
	return 0.14*i.Voice + 0.14*i.Evidence + 0.12*i.Burden + 0.11*i.Uncertainty +
		0.10*i.Reversibility + 0.13*i.LongTerm + 0.08*i.AI + 0.10*i.Accountability + 0.08*i.Redress
}

func main() {
	ideas := []EthicalIdea{
		{"AI-Assisted Service Triage", 0.42, 0.56, 0.44, 0.46, 0.50, 0.52, 0.38, 0.48, 0.36},
		{"Participatory Governance Council", 0.84, 0.72, 0.78, 0.70, 0.72, 0.74, 0.62, 0.76, 0.72},
		{"Workforce Restructuring Plan", 0.38, 0.58, 0.40, 0.44, 0.36, 0.42, 0.40, 0.46, 0.34},
	}

	for _, i := range ideas {
		score := Legitimacy(i)
		fmt.Printf("%s | ethical legitimacy %.3f | ethical risk %.3f\n", i.Name, score, 1-score)
	}
}
