// Efficient assumption scoring example.
// Compile: g++ assumption_score.cpp -std=c++17 -O2 -o assumption_score
// Run: ./assumption_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Assumption {
    std::string id;
    double criticality;
    double uncertainty;
    double evidence_strength;
    double evidence_relevance;
    double evidence_transferability;
    double testability;
    double stakeholder_sensitivity;
    double system_sensitivity;
};

double evidence_composite(const Assumption& a) {
    return 0.40 * a.evidence_strength +
           0.30 * a.evidence_relevance +
           0.30 * a.evidence_transferability;
}

double evidence_adjusted_risk(const Assumption& a) {
    return a.criticality * a.uncertainty * (1.0 - evidence_composite(a));
}

double learning_value(const Assumption& a) {
    return 0.34 * evidence_adjusted_risk(a) +
           0.24 * a.testability +
           0.18 * a.stakeholder_sensitivity +
           0.14 * a.system_sensitivity +
           0.10 * a.criticality;
}

int main() {
    std::vector<Assumption> assumptions = {
        {"A001", 0.86, 0.70, 0.38, 0.62, 0.54, 0.78, 0.72, 0.70},
        {"A004", 0.90, 0.72, 0.34, 0.72, 0.60, 0.74, 0.94, 0.76},
        {"A015", 0.86, 0.66, 0.38, 0.62, 0.52, 0.62, 0.70, 0.74}
    };

    std::sort(assumptions.begin(), assumptions.end(), [](const Assumption& a, const Assumption& b) {
        return evidence_adjusted_risk(a) > evidence_adjusted_risk(b);
    });

    for (const auto& a : assumptions) {
        std::cout << a.id
                  << " | risk " << evidence_adjusted_risk(a)
                  << " | learning " << learning_value(a) << "\n";
    }

    return 0;
}
