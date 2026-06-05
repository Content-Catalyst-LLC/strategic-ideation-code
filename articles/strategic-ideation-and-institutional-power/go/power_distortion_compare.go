// Strategic institutional power comparison utility scaffold.
// Run: go run power_distortion_compare.go

package main

import "fmt"

type PowerIdea struct {
	Name           string
	Merit          float64
	Evidence       float64
	Sponsorship    float64
	ResourceFit    float64
	Stakeholder    float64
	Dissent        float64
	Classification float64
	PowerAlignment float64
	Advancement    float64
}

func MeritScore(i PowerIdea) float64 {
	return 0.32*i.Merit + 0.24*i.Evidence + 0.18*i.Stakeholder + 0.14*i.Dissent + 0.12*i.Classification
}

func SupportScore(i PowerIdea) float64 {
	return 0.30*i.Sponsorship + 0.25*i.ResourceFit + 0.25*i.PowerAlignment + 0.20*i.Advancement
}

func main() {
	ideas := []PowerIdea{
		{"Participatory Governance Model", 0.78, 0.72, 0.54, 0.58, 0.78, 0.72, 0.76, 0.46, 0.52},
		{"Executive Dashboard Expansion", 0.62, 0.60, 0.86, 0.82, 0.42, 0.46, 0.58, 0.84, 0.82},
		{"Cost Consolidation Plan", 0.58, 0.52, 0.82, 0.80, 0.34, 0.38, 0.46, 0.86, 0.80},
	}

	for _, i := range ideas {
		merit := MeritScore(i)
		support := SupportScore(i)
		fmt.Printf("%s | merit %.3f | institutional support %.3f | power distortion %.3f\n", i.Name, merit, support, support-merit)
	}
}
