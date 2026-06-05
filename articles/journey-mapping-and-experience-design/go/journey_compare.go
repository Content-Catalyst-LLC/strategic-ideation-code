// Experience-quality evaluation utility scaffold.
// Run: go run journey_compare.go

package main

import "fmt"

type Journey struct {
	ID                  string
	Clarity             float64
	EmotionalConfidence float64
	Friction            float64
	TransitionQuality   float64
	Accessibility       float64
	Trust               float64
	CompletionSupport   float64
	BackstageAlignment  float64
	MeasurementQuality  float64
}

func JourneyProfile(j Journey) float64 {
	return 0.15*j.Clarity +
		0.12*j.EmotionalConfidence -
		0.18*j.Friction +
		0.14*j.TransitionQuality +
		0.12*j.Accessibility +
		0.12*j.Trust +
		0.10*j.CompletionSupport +
		0.10*j.BackstageAlignment +
		0.07*j.MeasurementQuality
}

func RedesignNeed(j Journey) float64 {
	return 0.22*j.Friction +
		0.16*(1-j.TransitionQuality) +
		0.14*(1-j.Accessibility) +
		0.13*(1-j.Trust) +
		0.12*(1-j.Clarity) +
		0.11*(1-j.BackstageAlignment) +
		0.07*(1-j.CompletionSupport) +
		0.05*(1-j.MeasurementQuality)
}

func Recommendation(j Journey) string {
	if JourneyProfile(j) >= 0.58 {
		return "strong_experience_design_profile"
	}
	if RedesignNeed(j) >= 0.62 {
		return "high_redesign_priority"
	}
	if j.TransitionQuality < 0.45 {
		return "transition_and_handoff_failure"
	}
	return "developing_journey_quality"
}

func main() {
	journeys := []Journey{
		{"J001", 0.36, 0.31, 0.82, 0.28, 0.34, 0.30, 0.34, 0.30, 0.38},
		{"J005", 0.81, 0.79, 0.28, 0.82, 0.88, 0.84, 0.86, 0.78, 0.76},
		{"J007", 0.54, 0.45, 0.72, 0.36, 0.50, 0.44, 0.52, 0.34, 0.46},
	}

	for _, j := range journeys {
		fmt.Printf("%s | journey profile %.3f | redesign need %.3f | %s\n",
			j.ID,
			JourneyProfile(j),
			RedesignNeed(j),
			Recommendation(j))
	}
}
