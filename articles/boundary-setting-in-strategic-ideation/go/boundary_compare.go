// Boundary comparison utility scaffold.
// Run: go run boundary_compare.go

package main

import "fmt"

type Boundary struct {
	ID            string
	Problem       float64
	System        float64
	Stakeholder   float64
	Causal        float64
	Temporal      float64
	Institutional float64
	Evidence      float64
	Ethical       float64
	Revision      float64
	Actionability float64
}

func BoundaryQuality(b Boundary) float64 {
	return 0.12*b.Problem +
		0.13*b.System +
		0.14*b.Stakeholder +
		0.14*b.Causal +
		0.12*b.Temporal +
		0.11*b.Institutional +
		0.11*b.Evidence +
		0.10*b.Ethical +
		0.09*b.Revision +
		0.04*b.Actionability
}

func Diagnosis(b Boundary) string {
	q := BoundaryQuality(b)
	if q >= 0.78 {
		return "strong_boundary_design"
	}
	if b.Stakeholder < 0.40 {
		return "stakeholder_exclusion_risk"
	}
	if b.Temporal < 0.40 {
		return "temporal_boundary_risk"
	}
	if b.Causal < 0.45 {
		return "causal_boundary_risk"
	}
	return "usable_with_boundary_review"
}

func main() {
	boundaries := []Boundary{
		{"B001", 0.62, 0.38, 0.34, 0.42, 0.38, 0.50, 0.40, 0.32, 0.38, 0.82},
		{"B003", 0.82, 0.90, 0.72, 0.88, 0.76, 0.78, 0.74, 0.70, 0.72, 0.58},
		{"B005", 0.84, 0.86, 0.82, 0.82, 0.84, 0.80, 0.86, 0.84, 0.90, 0.66},
	}

	for _, boundary := range boundaries {
		fmt.Printf("%s | %.3f | %s\n",
			boundary.ID,
			BoundaryQuality(boundary),
			Diagnosis(boundary))
	}
}
