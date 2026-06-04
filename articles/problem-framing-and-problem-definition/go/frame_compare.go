// Frame-comparison utility scaffold.
// Run: go run frame_compare.go

package main

import "fmt"

type Frame struct {
	ID            string
	Boundary      float64
	Stakeholder   float64
	Systems       float64
	Causal        float64
	Assumptions   float64
	Reframing     float64
	Actionability float64
	LockIn        float64
	Politics      float64
}

func Score(f Frame) float64 {
	return 0.16*f.Boundary +
		0.15*f.Stakeholder +
		0.15*f.Systems +
		0.16*f.Causal +
		0.12*f.Assumptions +
		0.13*f.Reframing +
		0.11*f.Actionability -
		0.10*f.LockIn -
		0.08*f.Politics
}

func SymptomRisk(f Frame) float64 {
	boundaryGap := 0.70 - f.Boundary
	if boundaryGap < 0 {
		boundaryGap = 0
	}
	return (1.0-f.Causal)*0.30 +
		(1.0-f.Systems)*0.25 +
		boundaryGap*0.20 +
		f.LockIn*0.15 +
		f.Politics*0.10
}

func Recommendation(f Frame) string {
	if Score(f) >= 0.68 {
		return "strong_problem_framing_capacity"
	}
	if SymptomRisk(f) >= 0.62 {
		return "symptom_or_convenience_frame_risk"
	}
	if f.Boundary < 0.45 {
		return "boundary_review_required"
	}
	return "develop_with_frame_comparison"
}

func main() {
	frames := []Frame{
		{"F001", 0.28, 0.34, 0.26, 0.31, 0.24, 0.22, 0.62, 0.82, 0.70},
		{"F003", 0.86, 0.79, 0.91, 0.84, 0.78, 0.82, 0.72, 0.32, 0.34},
		{"F005", 0.82, 0.92, 0.78, 0.74, 0.76, 0.80, 0.74, 0.34, 0.30},
	}

	for _, frame := range frames {
		fmt.Printf("%s | %.3f | %.3f | %s\n", frame.ID, Score(frame), SymptomRisk(frame), Recommendation(frame))
	}
}
