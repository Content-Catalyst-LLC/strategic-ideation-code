// Theory-of-change evaluation utility scaffold.
// Run: go run theory_compare.go

package main

import "fmt"

type Link struct {
	ID                 string
	MechanismClarity   float64
	EvidenceStrength   float64
	ActorDependency    float64
	CapacityDependency float64
	SystemDependency   float64
	EthicalDependency  float64
	FailureConsequence float64
	Testability        float64
}

func LinkRisk(l Link) float64 {
	return 0.16*(1-l.MechanismClarity) +
		0.18*(1-l.EvidenceStrength) +
		0.13*l.ActorDependency +
		0.11*l.CapacityDependency +
		0.14*l.SystemDependency +
		0.12*l.EthicalDependency +
		0.16*l.FailureConsequence
}

func TestPriority(l Link) float64 {
	return LinkRisk(l) * l.Testability
}

func Recommendation(l Link) string {
	if LinkRisk(l) >= 0.62 && l.Testability >= 0.62 {
		return "test_first"
	}
	if LinkRisk(l) >= 0.62 {
		return "reduce_commitment_before_scaling"
	}
	if l.EvidenceStrength <= 0.42 {
		return "evidence_gap"
	}
	return "monitor"
}

func main() {
	links := []Link{
		{"L002", 0.66, 0.38, 0.86, 0.62, 0.58, 0.52, 0.80, 0.78},
		{"L004", 0.72, 0.44, 0.82, 0.58, 0.68, 0.90, 0.86, 0.74},
		{"L009", 0.48, 0.32, 0.62, 0.48, 0.64, 0.60, 0.78, 0.58},
	}

	for _, link := range links {
		fmt.Printf("%s | link risk %.3f | test priority %.3f | %s\n",
			link.ID,
			LinkRisk(link),
			TestPriority(link),
			Recommendation(link))
	}
}
