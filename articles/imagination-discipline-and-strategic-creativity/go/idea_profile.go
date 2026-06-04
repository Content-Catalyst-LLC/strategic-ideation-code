// Idea-profile comparison utility scaffold.
// Run: go run idea_profile.go

package main

import "fmt"

type Idea struct {
	ID          string
	Novelty     float64
	Relevance   float64
	Coherence   float64
	Mechanism   float64
	Testability float64
	Stakeholder float64
	Systems     float64
	Development float64
	Risk        float64
	Revision    float64
}

func Score(i Idea) float64 {
	return 0.14*i.Novelty +
		0.16*i.Relevance +
		0.13*i.Coherence +
		0.14*i.Mechanism +
		0.11*i.Testability +
		0.13*i.Stakeholder +
		0.13*i.Systems +
		0.12*i.Development +
		0.08*i.Revision -
		0.12*i.Risk
}

func NoveltyTheaterRisk(i Idea) float64 {
	return i.Novelty * (1.0 - ((i.Mechanism + i.Stakeholder + i.Systems) / 3.0))
}

func Recommendation(i Idea) string {
	if NoveltyTheaterRisk(i) >= 0.42 {
		return "novelty_theater_review"
	}
	if i.Stakeholder < 0.45 {
		return "stakeholder_grounding_review"
	}
	if i.Systems < 0.50 {
		return "systems_fit_review"
	}
	if Score(i) >= 0.70 {
		return "strong_strategic_creativity_candidate"
	}
	return "develop_with_testing"
}

func main() {
	ideas := []Idea{
		{"I002", 0.72, 0.86, 0.78, 0.80, 0.70, 0.92, 0.78, 0.82, 0.56, 0.82},
		{"I005", 0.76, 0.88, 0.82, 0.84, 0.66, 0.70, 0.90, 0.86, 0.66, 0.86},
		{"I009", 0.70, 0.50, 0.52, 0.34, 0.46, 0.30, 0.32, 0.42, 0.40, 0.38},
	}

	for _, idea := range ideas {
		fmt.Printf("%s | %.3f | %.3f | %s\n", idea.ID, Score(idea), NoveltyTheaterRisk(idea), Recommendation(idea))
	}
}
