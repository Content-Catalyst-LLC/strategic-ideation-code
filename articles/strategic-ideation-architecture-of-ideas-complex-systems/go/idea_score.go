package main

import "fmt"

func weightedScore(values []float64, weights []float64) float64 {
	score := 0.0

	for i := range values {
		score += values[i] * weights[i]
	}

	return score
}

func main() {
	values := []float64{0.62, 0.86, 0.68, 0.88, 0.74, 0.35, 0.63}
	weights := []float64{0.16, 0.20, 0.16, 0.20, 0.14, -0.08, 0.14}

	fmt.Println("Synthetic strategic idea score:")
	fmt.Printf("%.3f\n", weightedScore(values, weights))
}
