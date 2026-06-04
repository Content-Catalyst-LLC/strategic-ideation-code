// Adaptive option comparison utility scaffold.
// Run: go run option_compare.go

package main

import "fmt"

type AdaptiveOption struct {
	ID                  string
	Robustness          float64
	OptionValue         float64
	Reversibility       float64
	LearningValue       float64
	DownsideProtection  float64
	ResourceIntensity   float64
	TimeToLearning      float64
	StrategicCoherence  float64
	LegitimacyRequirement float64
	EvidenceReadiness   float64
}

func Score(o AdaptiveOption) float64 {
	return 0.14*o.Robustness +
		0.15*o.OptionValue +
		0.12*o.Reversibility +
		0.14*o.LearningValue +
		0.12*o.DownsideProtection -
		0.10*o.ResourceIntensity -
		0.08*o.TimeToLearning +
		0.12*o.StrategicCoherence -
		0.08*o.LegitimacyRequirement +
		0.10*o.EvidenceReadiness
}

func Recommendation(o AdaptiveOption) string {
	if Score(o) >= 0.55 {
		return "priority_adaptive_option"
	}
	if o.LegitimacyRequirement >= 0.80 {
		return "add_legitimacy_safeguards"
	}
	if o.ResourceIntensity >= 0.65 {
		return "stage_commitment"
	}
	return "develop_or_monitor_option"
}

func main() {
	options := []AdaptiveOption{
		{"O002", 0.68, 0.82, 0.76, 0.86, 0.54, 0.46, 0.34, 0.74, 0.42, 0.64},
		{"O004", 0.76, 0.88, 0.58, 0.86, 0.74, 0.68, 0.56, 0.76, 0.76, 0.56},
		{"O006", 0.78, 0.76, 0.54, 0.66, 0.86, 0.72, 0.52, 0.70, 0.42, 0.66},
	}

	for _, option := range options {
		fmt.Printf("%s | %.3f | %s\n", option.ID, Score(option), Recommendation(option))
	}
}
