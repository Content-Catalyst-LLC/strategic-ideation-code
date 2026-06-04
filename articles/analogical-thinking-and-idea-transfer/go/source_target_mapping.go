// Source-target mapping utility scaffold.
// Run: go run source_target_mapping.go

package main

import "fmt"

type Mapping struct {
	ID                         string
	ActorCorrespondence        float64
	RelationCorrespondence     float64
	FlowCorrespondence         float64
	ConstraintCorrespondence   float64
	FeedbackCorrespondence     float64
	FailureModeCorrespondence  float64
	BreakpointVisibility       float64
	MappingConfidence          float64
}

func MappingScore(m Mapping) float64 {
	return 0.14*m.ActorCorrespondence +
		0.20*m.RelationCorrespondence +
		0.14*m.FlowCorrespondence +
		0.14*m.ConstraintCorrespondence +
		0.14*m.FeedbackCorrespondence +
		0.12*m.FailureModeCorrespondence +
		0.08*m.BreakpointVisibility +
		0.04*m.MappingConfidence
}

func Recommendation(m Mapping) string {
	if m.RelationCorrespondence < 0.50 {
		return "repair_relational_mapping"
	}
	if m.BreakpointVisibility < 0.45 {
		return "define_analogy_breakpoints"
	}
	if MappingScore(m) >= 0.72 {
		return "strong_mapping_candidate"
	}
	return "mapping_requires_review"
}

func main() {
	mappings := []Mapping{
		{"M001", 0.52, 0.34, 0.36, 0.42, 0.30, 0.28, 0.26, 0.36},
		{"M005", 0.76, 0.88, 0.80, 0.86, 0.82, 0.84, 0.86, 0.84},
		{"M007", 0.80, 0.88, 0.86, 0.78, 0.84, 0.82, 0.80, 0.86},
	}

	for _, mapping := range mappings {
		fmt.Printf("%s | %.3f | %s\n", mapping.ID, MappingScore(mapping), Recommendation(mapping))
	}
}
