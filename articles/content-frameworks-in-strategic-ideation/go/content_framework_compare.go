// Strategic content framework comparison utility scaffold.
// Run: go run content_framework_compare.go

package main

import "fmt"

type Framework struct {
	Name       string
	Structure  float64
	Clarity    float64
	Evidence   float64
	Assumptions float64
	Narrative  float64
	Decision   float64
	Modularity float64
	Reuse      float64
	Governance float64
	Ethics     float64
}

func Score(f Framework) float64 {
	return 0.11*f.Structure + 0.11*f.Clarity + 0.12*f.Evidence + 0.10*f.Assumptions +
		0.10*f.Narrative + 0.13*f.Decision + 0.10*f.Modularity +
		0.10*f.Reuse + 0.08*f.Governance + 0.05*f.Ethics
}

func main() {
	frameworks := []Framework{
		{"Idea Record Framework", 0.76, 0.72, 0.66, 0.68, 0.62, 0.64, 0.74, 0.72, 0.66, 0.60},
		{"Decision Memo Framework", 0.82, 0.76, 0.80, 0.78, 0.74, 0.86, 0.66, 0.68, 0.72, 0.72},
		{"AI-Assisted Ideation Framework", 0.62, 0.56, 0.50, 0.48, 0.58, 0.54, 0.60, 0.58, 0.46, 0.42},
	}

	for _, f := range frameworks {
		score := Score(f)
		fmt.Printf("%s | framework strength %.3f | framework risk %.3f\n", f.Name, score, 1-score)
	}
}
