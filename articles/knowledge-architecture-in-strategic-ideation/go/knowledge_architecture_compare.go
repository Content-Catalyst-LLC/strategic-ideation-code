// Strategic knowledge architecture comparison utility scaffold.
// Run: go run knowledge_architecture_compare.go

package main

import "fmt"

type Idea struct {
	Name          string
	Taxonomy      float64
	Metadata      float64
	Semantics     float64
	Evidence      float64
	Assumptions   float64
	Relationships float64
	Retrieval     float64
	Memory        float64
	Stewardship   float64
	Ethics        float64
}

func Score(i Idea) float64 {
	return 0.11*i.Taxonomy + 0.12*i.Metadata + 0.11*i.Semantics + 0.12*i.Evidence +
		0.11*i.Assumptions + 0.11*i.Relationships + 0.12*i.Retrieval +
		0.09*i.Memory + 0.07*i.Stewardship + 0.04*i.Ethics
}

func main() {
	ideas := []Idea{
		{"Community Data Stewardship", 0.74, 0.70, 0.76, 0.66, 0.68, 0.72, 0.70, 0.62, 0.64, 0.78},
		{"AI-Assisted Scenario Library", 0.62, 0.58, 0.54, 0.52, 0.50, 0.58, 0.54, 0.46, 0.48, 0.46},
		{"Strategic Learning Repository", 0.78, 0.80, 0.82, 0.74, 0.72, 0.82, 0.84, 0.78, 0.76, 0.66},
	}

	for _, i := range ideas {
		score := Score(i)
		fmt.Printf("%s | architecture strength %.3f | architecture risk %.3f\n", i.Name, score, 1-score)
	}
}
