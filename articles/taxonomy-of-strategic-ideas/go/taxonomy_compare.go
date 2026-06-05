// Strategic taxonomy comparison utility scaffold.
// Run: go run taxonomy_compare.go

package main

import "fmt"

type TaxonomyRecord struct {
	Name          string
	Category      float64
	Level         float64
	Maturity      float64
	Evidence      float64
	Function      float64
	Relationships float64
	Retrieval     float64
	Governance    float64
	Ethics        float64
}

func Score(t TaxonomyRecord) float64 {
	return 0.13*t.Category + 0.11*t.Level + 0.11*t.Maturity + 0.12*t.Evidence +
		0.13*t.Function + 0.11*t.Relationships + 0.13*t.Retrieval +
		0.09*t.Governance + 0.07*t.Ethics
}

func main() {
	records := []TaxonomyRecord{
		{"Strategic Learning Repository", 0.78, 0.76, 0.72, 0.72, 0.80, 0.76, 0.82, 0.74, 0.66},
		{"Participatory Governance Prototype", 0.76, 0.74, 0.76, 0.70, 0.74, 0.72, 0.76, 0.70, 0.82},
		{"Advisory Panel Without Authority", 0.66, 0.62, 0.72, 0.62, 0.60, 0.66, 0.62, 0.56, 0.76},
	}

	for _, t := range records {
		score := Score(t)
		fmt.Printf("%s | taxonomy strength %.3f | taxonomy risk %.3f\n", t.Name, score, 1-score)
	}
}
