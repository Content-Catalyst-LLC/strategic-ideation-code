// Intervention comparison utility for second-order effects.
// Run: go run intervention_compare.go

package main

import "fmt"

type Intervention struct {
	ID            string
	FirstGain     float64
	Adaptation    float64
	Feedback      float64
	Delay         float64
	Burden        float64
	Gaming        float64
	Fragility     float64
	Learning      float64
	Legitimacy    float64
	Reversibility float64
}

func SecondOrderRisk(i Intervention) float64 {
	return 0.16*i.Adaptation +
		0.15*i.Feedback +
		0.14*i.Delay +
		0.15*i.Burden +
		0.14*i.Gaming +
		0.16*i.Fragility -
		0.10*i.Learning -
		0.06*i.Legitimacy -
		0.06*i.Reversibility
}

func FalseSuccessRisk(i Intervention) float64 {
	return 0.26*i.FirstGain +
		0.20*i.Fragility +
		0.16*i.Delay +
		0.14*i.Gaming +
		0.12*i.Burden -
		0.16*i.Learning
}

func Recommendation(i Intervention) string {
	if FalseSuccessRisk(i) >= 0.55 {
		return "false_first_order_success_risk"
	}
	if i.Gaming >= 0.70 {
		return "gaming_and_metric_distortion_risk"
	}
	if i.Burden >= 0.70 {
		return "burden_shift_risk"
	}
	if SecondOrderRisk(i) >= 0.50 {
		return "second_order_review_required"
	}
	return "monitor_with_learning_loop"
}

func main() {
	interventions := []Intervention{
		{"I001", 0.88, 0.76, 0.58, 0.69, 0.66, 0.52, 0.82, 0.38, 0.44, 0.42},
		{"I002", 0.71, 0.44, 0.51, 0.42, 0.34, 0.28, 0.39, 0.76, 0.72, 0.70},
		{"I003", 0.63, 0.81, 0.73, 0.57, 0.78, 0.74, 0.74, 0.42, 0.46, 0.38},
	}

	for _, intervention := range interventions {
		fmt.Printf("%s | %.3f | %.3f | %s\n",
			intervention.ID,
			SecondOrderRisk(intervention),
			FalseSuccessRisk(intervention),
			Recommendation(intervention))
	}
}
