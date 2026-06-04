// Reframing-evaluation utility scaffold.
// Run: go run reframing_evaluation.go

package main

import "fmt"

type LateralMove struct {
	ID                    string
	FrameDisruption       float64
	StrategicRelevance    float64
	ReconstructionQuality float64
	EvidencePathway       float64
	StakeholderFit        float64
	SystemsFit            float64
	NoveltyValue          float64
	DriftRisk             float64
}

func MoveScore(m LateralMove) float64 {
	return 0.16*m.FrameDisruption +
		0.18*m.StrategicRelevance +
		0.16*m.ReconstructionQuality +
		0.12*m.EvidencePathway +
		0.12*m.StakeholderFit +
		0.12*m.SystemsFit +
		0.10*m.NoveltyValue -
		0.14*m.DriftRisk
}

func Recommendation(m LateralMove) string {
	if m.DriftRisk >= 0.70 {
		return "high_drift_risk_reconstruction_required"
	}
	if m.ReconstructionQuality < 0.45 {
		return "reconstruct_before_evaluation"
	}
	if m.StakeholderFit < 0.40 {
		return "stakeholder_review_before_advancing"
	}
	if MoveScore(m) >= 0.62 {
		return "advance_to_reframe_review"
	}
	return "revise_or_hold_lateral_move"
}

func main() {
	moves := []LateralMove{
		{"M002", 0.78, 0.82, 0.64, 0.58, 0.62, 0.66, 0.70, 0.34},
		{"M008", 0.70, 0.86, 0.82, 0.78, 0.80, 0.88, 0.74, 0.22},
		{"M013", 0.80, 0.34, 0.22, 0.18, 0.26, 0.24, 0.86, 0.86},
	}

	for _, move := range moves {
		fmt.Printf("%s | %.3f | %s\n", move.ID, MoveScore(move), Recommendation(move))
	}
}
