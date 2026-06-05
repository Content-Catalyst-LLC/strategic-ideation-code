// Strategic sequencing comparison utility scaffold.
// Run: go run sequencing_compare.go

package main

import "fmt"

type Pathway struct {
	Name          string
	Capability    float64
	Evidence      float64
	Governance    float64
	Legitimacy    float64
	Dependency    float64
	Reversibility float64
	Capacity      float64
	Timing        float64
	Ethics        float64
}

func Score(p Pathway) float64 {
	return 0.16*p.Capability + 0.15*p.Evidence + 0.15*p.Governance + 0.14*p.Legitimacy -
		0.12*p.Dependency + 0.10*p.Reversibility - 0.10*p.Capacity + 0.08*p.Timing + 0.12*p.Ethics
}

func main() {
	pathways := []Pathway{
		{"Data Governance Foundation", 0.72, 0.66, 0.78, 0.62, 0.42, 0.70, 0.46, 0.52, 0.70},
		{"Full Platform Rollout", 0.52, 0.46, 0.48, 0.44, 0.82, 0.38, 0.84, 0.60, 0.42},
		{"Adaptive Rollout Sequence", 0.70, 0.68, 0.72, 0.74, 0.52, 0.76, 0.60, 0.66, 0.78},
	}

	for _, p := range pathways {
		fmt.Printf("%s | sequencing readiness %.3f\n", p.Name, Score(p))
	}
}
