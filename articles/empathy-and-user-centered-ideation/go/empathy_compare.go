// User-centered ideation evaluation utility scaffold.
// Run: go run empathy_compare.go

package main

import "fmt"

type Context struct {
	ID                 string
	Observation        float64
	Projection         float64
	UnmetNeed          float64
	StakeholderBreadth float64
	Reframing          float64
	Ethics             float64
	Systems            float64
	Decision           float64
	Memory             float64
}

func EmpathyProfile(c Context) float64 {
	return 0.16*c.Observation -
		0.14*c.Projection +
		0.16*c.UnmetNeed +
		0.12*c.StakeholderBreadth +
		0.16*c.Reframing +
		0.10*c.Ethics +
		0.10*c.Systems +
		0.14*c.Decision +
		0.10*c.Memory
}

func SuperficialityRisk(c Context) float64 {
	return 0.20*c.Projection +
		0.16*(1-c.Decision) +
		0.14*(1-c.Observation) +
		0.12*(1-c.UnmetNeed) +
		0.12*(1-c.Ethics) +
		0.10*(1-c.Systems) +
		0.08*(1-c.StakeholderBreadth) +
		0.08*(1-c.Memory)
}

func Recommendation(c Context) string {
	if EmpathyProfile(c) >= 0.64 {
		return "strong_user_centered_ideation_capability"
	}
	if SuperficialityRisk(c) >= 0.62 {
		return "high_empathy_theater_or_projection_risk"
	}
	if c.Decision < 0.42 {
		return "insight_not_linked_to_decisions"
	}
	return "developing_capability"
}

func main() {
	contexts := []Context{
		{"C001", 0.24, 0.84, 0.31, 0.28, 0.34, 0.38, 0.35, 0.32, 0.30},
		{"C004", 0.76, 0.48, 0.79, 0.90, 0.83, 0.86, 0.88, 0.78, 0.76},
		{"C005", 0.38, 0.72, 0.42, 0.36, 0.40, 0.32, 0.30, 0.24, 0.22},
	}

	for _, c := range contexts {
		fmt.Printf("%s | empathy profile %.3f | superficiality risk %.3f | %s\n",
			c.ID,
			EmpathyProfile(c),
			SuperficialityRisk(c),
			Recommendation(c))
	}
}
