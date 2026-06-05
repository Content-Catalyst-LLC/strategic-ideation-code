// Strategic implementation comparison utility scaffold.
// Run: go run implementation_compare.go

package main

import "fmt"

type ImplementationProfile struct {
	Name           string
	Goal           float64
	Coordination   float64
	Structure      float64
	Culture        float64
	Incentives     float64
	Resources      float64
	Communication float64
	Accountability float64
	Adaptation     float64
}

func Score(p ImplementationProfile) float64 {
	return 0.12*p.Goal + 0.15*p.Coordination + 0.12*p.Structure + 0.12*p.Culture +
		0.13*p.Incentives + 0.12*p.Resources + 0.11*p.Communication + 0.10*p.Accountability + 0.10*p.Adaptation
}

func main() {
	profiles := []ImplementationProfile{
		{"High-Intent Fragmented Organization", 0.70, 0.38, 0.44, 0.31, 0.29, 0.52, 0.41, 0.46, 0.36},
		{"Balanced Aligned Organization", 0.82, 0.81, 0.79, 0.78, 0.77, 0.82, 0.80, 0.76, 0.74},
		{"Adaptive Cross-Functional Organization", 0.78, 0.84, 0.73, 0.76, 0.71, 0.76, 0.78, 0.74, 0.83},
	}

	for _, p := range profiles {
		fmt.Printf("%s | implementation score %.3f\n", p.Name, Score(p))
	}
}
