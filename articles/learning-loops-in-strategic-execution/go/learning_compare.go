// Strategic learning loop comparison utility scaffold.
// Run: go run learning_compare.go

package main

import "fmt"

type Context struct {
	Name           string
	Feedback       float64
	Assumptions    float64
	Interpretation float64
	Authority      float64
	Closure        float64
	Memory         float64
	Safety         float64
	Scaling        float64
	Ethics         float64
}

func Score(c Context) float64 {
	return 0.13*c.Feedback + 0.13*c.Assumptions + 0.12*c.Interpretation +
		0.14*c.Authority + 0.14*c.Closure + 0.10*c.Memory +
		0.09*c.Safety + 0.08*c.Scaling + 0.07*c.Ethics
}

func main() {
	contexts := []Context{
		{"Reporting-Heavy Organization", 0.62, 0.42, 0.46, 0.38, 0.34, 0.36, 0.44, 0.40, 0.50},
		{"Adaptive Learning Organization", 0.84, 0.82, 0.80, 0.78, 0.82, 0.76, 0.78, 0.74, 0.80},
		{"Pilot-Rich Memory-Poor Organization", 0.72, 0.60, 0.62, 0.56, 0.48, 0.30, 0.58, 0.36, 0.56},
	}

	for _, c := range contexts {
		score := Score(c)
		fmt.Printf("%s | learning loop strength %.3f | learning debt %.3f\n", c.Name, score, 1-score)
	}
}
