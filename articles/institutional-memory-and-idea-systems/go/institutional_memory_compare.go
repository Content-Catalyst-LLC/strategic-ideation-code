// Strategic institutional memory comparison utility scaffold.
// Run: go run institutional_memory_compare.go

package main

import "fmt"

type MemorySystem struct {
	Name        string
	Capture     float64
	Metadata    float64
	Context     float64
	Decisions   float64
	Learning    float64
	Retrieval   float64
	Reuse       float64
	Stewardship float64
	Continuity  float64
	Ethics      float64
}

func Score(m MemorySystem) float64 {
	return 0.10*m.Capture + 0.12*m.Metadata + 0.12*m.Context + 0.13*m.Decisions +
		0.12*m.Learning + 0.12*m.Retrieval + 0.10*m.Reuse +
		0.08*m.Stewardship + 0.06*m.Continuity + 0.05*m.Ethics
}

func main() {
	systems := []MemorySystem{
		{"Strategic Idea Repository", 0.72, 0.80, 0.76, 0.66, 0.68, 0.78, 0.80, 0.72, 0.70, 0.62},
		{"Decision Memory", 0.70, 0.74, 0.82, 0.86, 0.72, 0.74, 0.76, 0.70, 0.72, 0.70},
		{"Retired Ideas Archive", 0.58, 0.54, 0.56, 0.58, 0.48, 0.52, 0.60, 0.50, 0.48, 0.58},
	}

	for _, m := range systems {
		score := Score(m)
		fmt.Printf("%s | memory strength %.3f | failure risk %.3f\n", m.Name, score, 1-score)
	}
}
