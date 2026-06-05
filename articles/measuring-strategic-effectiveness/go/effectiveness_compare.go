// Strategic effectiveness comparison utility scaffold.
// Run: go run effectiveness_compare.go

package main

import "fmt"

type Strategy struct {
	Name         string
	Performance  float64
	Alignment    float64
	Resilience   float64
	Adaptability float64
	Impact       float64
	Learning     float64
	Confidence   float64
	Ethics       float64
}

func Score(s Strategy) float64 {
	return 0.20*s.Performance + 0.15*s.Alignment + 0.16*s.Resilience + 0.15*s.Adaptability +
		0.14*s.Impact + 0.10*s.Learning + 0.05*s.Confidence + 0.05*s.Ethics
}

func main() {
	strategies := []Strategy{
		{"Efficiency-Led Strategy", 0.84, 0.58, 0.42, 0.46, 0.51, 0.42, 0.66, 0.48},
		{"Balanced Capability Strategy", 0.72, 0.79, 0.76, 0.78, 0.73, 0.76, 0.74, 0.72},
		{"Adaptive Learning Strategy", 0.70, 0.76, 0.78, 0.88, 0.74, 0.90, 0.70, 0.76},
	}

	for _, s := range strategies {
		score := Score(s)
		fmt.Printf("%s | score %.3f | confidence-adjusted %.3f\n", s.Name, score, score*s.Confidence)
	}
}
