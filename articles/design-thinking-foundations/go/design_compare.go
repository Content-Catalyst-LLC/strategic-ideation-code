// Design thinking capability utility scaffold.
// Run: go run design_compare.go

package main

import "fmt"

type DesignContext struct {
	ID            string
	Empathy       float64
	Reframing     float64
	Divergence    float64
	Convergence   float64
	Prototyping   float64
	Testing       float64
	Systems       float64
	Ethics        float64
	Decision      float64
	Adaptability  float64
	Memory        float64
}

func Capability(c DesignContext) float64 {
	return 0.12*c.Empathy +
		0.13*c.Reframing +
		0.10*c.Divergence +
		0.10*c.Convergence +
		0.12*c.Prototyping +
		0.12*c.Testing +
		0.11*c.Systems +
		0.10*c.Ethics +
		0.10*c.Decision +
		0.06*c.Adaptability +
		0.04*c.Memory
}

func SuperficialityRisk(c DesignContext) float64 {
	return 0.18*(1-c.Empathy) +
		0.14*(1-c.Reframing) +
		0.12*(1-c.Testing) +
		0.12*(1-c.Systems) +
		0.12*(1-c.Ethics) +
		0.16*(1-c.Decision) +
		0.10*(1-c.Memory) +
		0.06*(1-c.Adaptability)
}

func Recommendation(c DesignContext) string {
	if Capability(c) >= 0.72 {
		return "strong_design_thinking_capability"
	}
	if SuperficialityRisk(c) >= 0.62 {
		return "high_superficiality_risk"
	}
	if c.Decision < 0.45 {
		return "weak_decision_linkage"
	}
	return "developing_capability"
}

func main() {
	contexts := []DesignContext{
		{"C001", 0.28, 0.31, 0.36, 0.58, 0.24, 0.29, 0.35, 0.42, 0.36, 0.33, 0.40},
		{"C003", 0.81, 0.84, 0.86, 0.74, 0.88, 0.86, 0.72, 0.74, 0.78, 0.89, 0.76},
		{"C004", 0.39, 0.34, 0.68, 0.38, 0.41, 0.36, 0.30, 0.34, 0.28, 0.42, 0.24},
	}

	for _, c := range contexts {
		fmt.Printf("%s | capability %.3f | superficiality risk %.3f | %s\n",
			c.ID,
			Capability(c),
			SuperficialityRisk(c),
			Recommendation(c))
	}
}
