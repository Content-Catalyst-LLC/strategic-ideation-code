// Strategic portfolio comparison utility scaffold.
// Run: go run portfolio_compare.go

package main

import "fmt"

type IdeaProfile struct {
	Name              string
	Impact            float64
	Risk              float64
	Learning          float64
	OptionValue       float64
	StrategicFit      float64
	CapacityDemand    float64
	EthicalResilience float64
}

func PortfolioContribution(i IdeaProfile) float64 {
	return 0.18*i.Impact +
		0.18*i.StrategicFit +
		0.16*i.Learning +
		0.16*i.OptionValue +
		0.14*i.EthicalResilience -
		0.10*i.Risk -
		0.08*i.CapacityDemand
}

func OverloadWarning(i IdeaProfile) float64 {
	return 0.34*i.CapacityDemand +
		0.24*i.Risk +
		0.16*(1-i.StrategicFit) +
		0.14*(1-i.EthicalResilience) +
		0.12*(1-i.OptionValue)
}

func main() {
	ideas := []IdeaProfile{
		{"Core Process Improvement", 0.68, 0.32, 0.38, 0.34, 0.72, 0.44, 0.58},
		{"Exploratory Market Experiment", 0.58, 0.56, 0.84, 0.76, 0.62, 0.38, 0.62},
		{"Transformational Strategic Bet", 0.88, 0.78, 0.70, 0.62, 0.70, 0.86, 0.48},
	}

	for _, idea := range ideas {
		fmt.Printf("%s | contribution %.3f | overload warning %.3f\n",
			idea.Name, PortfolioContribution(idea), OverloadWarning(idea))
	}
}
