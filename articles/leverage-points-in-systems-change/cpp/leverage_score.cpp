// Efficient leverage-point scoring example.
// Compile: g++ leverage_score.cpp -std=c++17 -O2 -o leverage_score
// Run: ./leverage_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct LeveragePoint {
    std::string id;
    double implementation_ease;
    double structural_depth;
    double system_sensitivity;
    double feedback_influence;
    double information_effect;
    double rule_power;
    double goal_alignment;
    double paradigm_relevance;
    double transformative_potential;
    double legitimacy_requirement;
    double unintended_risk;
    double learning_capacity;
};

double leverage_score(const LeveragePoint& l) {
    return 0.06 * l.implementation_ease
         + 0.16 * l.structural_depth
         + 0.14 * l.system_sensitivity
         + 0.13 * l.feedback_influence
         + 0.11 * l.information_effect
         + 0.13 * l.rule_power
         + 0.13 * l.goal_alignment
         + 0.08 * l.paradigm_relevance
         + 0.14 * l.transformative_potential
         + 0.08 * l.learning_capacity
         - 0.06 * l.unintended_risk;
}

double governance_need(const LeveragePoint& l) {
    return 0.26 * l.legitimacy_requirement
         + 0.24 * l.unintended_risk
         + 0.22 * l.transformative_potential
         + 0.14 * (1.0 - l.implementation_ease)
         + 0.14 * l.paradigm_relevance;
}

int main() {
    std::vector<LeveragePoint> points = {
        {"L001", 0.86, 0.22, 0.28, 0.28, 0.31, 0.20, 0.28, 0.16, 0.24, 0.24, 0.26, 0.34},
        {"L006", 0.44, 0.82, 0.82, 0.76, 0.66, 0.90, 0.78, 0.58, 0.82, 0.72, 0.70, 0.70},
        {"L008", 0.21, 0.96, 0.88, 0.82, 0.60, 0.78, 0.96, 0.98, 0.96, 0.90, 0.82, 0.78}
    };

    std::sort(points.begin(), points.end(), [](const LeveragePoint& a, const LeveragePoint& b) {
        return leverage_score(a) > leverage_score(b);
    });

    for (const auto& point : points) {
        std::cout << point.id
                  << " | leverage " << leverage_score(point)
                  << " | governance need " << governance_need(point) << "\n";
    }

    return 0;
}
