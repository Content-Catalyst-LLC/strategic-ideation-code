// Efficient idea-to-strategy conversion scoring example.
// Compile: g++ strategy_conversion_score.cpp -std=c++17 -O2 -o strategy_conversion_score
// Run: ./strategy_conversion_score

#include <iostream>
#include <string>
#include <vector>

struct Initiative {
    std::string name;
    double feasibility;
    double viability;
    double desirability;
    double integration_difficulty;
    double execution_readiness;
    double strategic_fit;
    double evidence_confidence;
    double ethical_resilience;
};

double conversion_score(const Initiative& i) {
    return 0.16 * i.feasibility +
           0.18 * i.viability +
           0.16 * i.desirability -
           0.12 * i.integration_difficulty +
           0.16 * i.execution_readiness +
           0.12 * i.strategic_fit +
           0.08 * i.evidence_confidence +
           0.06 * i.ethical_resilience;
}

int main() {
    std::vector<Initiative> initiatives = {
        {"High-Idea Low-Execution Concept", 0.78, 0.38, 0.82, 0.72, 0.29, 0.62, 0.42, 0.54},
        {"Balanced Strategic Initiative", 0.74, 0.79, 0.77, 0.44, 0.81, 0.84, 0.76, 0.72},
        {"Integration-Challenged Initiative", 0.69, 0.71, 0.84, 0.83, 0.52, 0.76, 0.58, 0.60}
    };

    for (const auto& i : initiatives) {
        double score = conversion_score(i);
        std::cout << i.name
                  << " | score " << score
                  << " | confidence-adjusted " << score * i.evidence_confidence << "\n";
    }

    return 0;
}
