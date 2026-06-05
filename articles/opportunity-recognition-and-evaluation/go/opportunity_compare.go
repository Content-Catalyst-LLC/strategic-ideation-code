// Strategic opportunity comparison utility scaffold.
// Run: go run opportunity_compare.go

package main

import "fmt"

type OpportunityProfile struct {
	Name         string
	Signal       float64
	Capability   float64
	Desirability float64
	Viability    float64
	Timing       float64
	Learning     float64
	OptionValue  float64
	StrategicFit float64
	Ethics       float64
	Risk         float64
	Confidence   float64
}

func ProfileScore(o OpportunityProfile) float64 {
	return 0.13*o.Signal +
		0.14*o.Capability +
		0.12*o.Desirability +
		0.12*o.Viability +
		0.10*o.Timing +
		0.12*o.Learning +
		0.11*o.OptionValue +
		0.10*o.StrategicFit +
		0.10*o.Ethics -
		0.14*o.Risk
}

func main() {
	opportunities := []OpportunityProfile{
		{"Emerging Technology Adjacency", 0.74, 0.78, 0.72, 0.71, 0.76, 0.70, 0.66, 0.78, 0.62, 0.46, 0.68},
		{"High-Hype Weak-Fit Opportunity", 0.86, 0.31, 0.77, 0.39, 0.48, 0.62, 0.44, 0.40, 0.42, 0.78, 0.38},
		{"Slow-Build Sustainability Opportunity", 0.62, 0.73, 0.81, 0.74, 0.67, 0.64, 0.72, 0.76, 0.82, 0.41, 0.66},
	}

	for _, o := range opportunities {
		score := ProfileScore(o)
		fmt.Printf("%s | score %.3f | confidence-adjusted %.3f\n", o.Name, score, score*o.Confidence)
	}
}
