// Strategic interaction comparison utility scaffold.
// Run: go run game_theory_compare.go

package main

import "fmt"

type Setting struct {
	Name                  string
	Rivalry               float64
	Coordination          float64
	InformationAsymmetry  float64
	Retaliation           float64
	InstitutionalSupport  float64
	BehavioralRealism     float64
	MechanismDesign       float64
	EthicalComplexity      float64
}

func MechanismOpportunity(s Setting) float64 {
	return 0.30*s.MechanismDesign +
		0.18*s.Coordination +
		0.16*s.InformationAsymmetry +
		0.14*s.EthicalComplexity +
		0.12*s.InstitutionalSupport +
		0.10*s.BehavioralRealism
}

func CooperationFragility(s Setting) float64 {
	return 0.22*s.Rivalry +
		0.20*s.Retaliation +
		0.16*s.InformationAsymmetry +
		0.12*s.EthicalComplexity -
		0.15*s.InstitutionalSupport -
		0.15*s.Coordination
}

func main() {
	settings := []Setting{
		{"Price Competition Environment", 0.84, 0.28, 0.44, 0.76, 0.39, 0.52, 0.42, 0.46},
		{"Standards Coordination Environment", 0.36, 0.86, 0.31, 0.24, 0.73, 0.68, 0.78, 0.54},
		{"Platform Ecosystem Environment", 0.71, 0.74, 0.69, 0.58, 0.57, 0.74, 0.82, 0.76},
	}

	for _, s := range settings {
		fmt.Printf("%s | mechanism opportunity %.3f | cooperation fragility %.3f\n",
			s.Name, MechanismOpportunity(s), CooperationFragility(s))
	}
}
