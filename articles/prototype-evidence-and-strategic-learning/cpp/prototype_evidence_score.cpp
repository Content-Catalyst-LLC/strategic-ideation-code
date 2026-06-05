// Efficient prototype evidence scoring example.
// Compile: g++ prototype_evidence_score.cpp -std=c++17 -O2 -o prototype_evidence_score
// Run: ./prototype_evidence_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct PrototypeSystem {
    std::string id;
    double assumption_clarity;
    double learning_target_fit;
    double evidence_quality;
    double behavioral_grounding;
    double context_realism;
    double systems_awareness;
    double decision_linkage;
    double ethical_review;
    double learning_memory;
};

double learning_quality(const PrototypeSystem& s) {
    return 0.13 * s.assumption_clarity +
           0.13 * s.learning_target_fit +
           0.15 * s.evidence_quality +
           0.13 * s.behavioral_grounding +
           0.11 * s.context_realism +
           0.11 * s.systems_awareness +
           0.11 * s.decision_linkage +
           0.07 * s.ethical_review +
           0.06 * s.learning_memory;
}

double validation_theater_risk(const PrototypeSystem& s) {
    return 0.17 * (1.0 - s.assumption_clarity) +
           0.16 * (1.0 - s.evidence_quality) +
           0.14 * (1.0 - s.behavioral_grounding) +
           0.13 * (1.0 - s.decision_linkage) +
           0.12 * (1.0 - s.learning_memory) +
           0.11 * (1.0 - s.systems_awareness) +
           0.09 * (1.0 - s.ethical_review) +
           0.08 * (1.0 - s.context_realism);
}

int main() {
    std::vector<PrototypeSystem> systems = {
        {"PE001", 0.30, 0.28, 0.26, 0.22, 0.34, 0.24, 0.20, 0.28, 0.22},
        {"PE004", 0.84, 0.82, 0.84, 0.76, 0.80, 0.88, 0.82, 0.72, 0.82},
        {"PE007", 0.52, 0.46, 0.40, 0.26, 0.32, 0.30, 0.38, 0.36, 0.34}
    };

    std::sort(systems.begin(), systems.end(), [](const PrototypeSystem& a, const PrototypeSystem& b) {
        return learning_quality(a) > learning_quality(b);
    });

    for (const auto& s : systems) {
        std::cout << s.id
                  << " | learning quality " << learning_quality(s)
                  << " | validation theater risk " << validation_theater_risk(s) << "\n";
    }

    return 0;
}
