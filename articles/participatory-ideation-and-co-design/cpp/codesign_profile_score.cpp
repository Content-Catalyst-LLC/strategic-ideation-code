// Efficient co-design profile scoring example.
// Compile: g++ codesign_profile_score.cpp -std=c++17 -O2 -o codesign_profile_score
// Run: ./codesign_profile_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct ParticipationSystem {
    std::string id;
    double representation;
    double influence;
    double accessibility;
    double reciprocity;
    double power_awareness;
    double knowledge_integration;
    double decision_linkage;
    double accountability;
    double learning_memory;
};

double participation_quality(const ParticipationSystem& s) {
    return 0.13 * s.representation +
           0.15 * s.influence +
           0.11 * s.accessibility +
           0.11 * s.reciprocity +
           0.13 * s.power_awareness +
           0.12 * s.knowledge_integration +
           0.11 * s.decision_linkage +
           0.10 * s.accountability +
           0.04 * s.learning_memory;
}

double tokenism_risk(const ParticipationSystem& s) {
    return 0.16 * (1.0 - s.influence) +
           0.14 * (1.0 - s.decision_linkage) +
           0.14 * (1.0 - s.accountability) +
           0.13 * (1.0 - s.reciprocity) +
           0.13 * (1.0 - s.power_awareness) +
           0.11 * (1.0 - s.representation) +
           0.10 * (1.0 - s.accessibility) +
           0.09 * (1.0 - s.learning_memory);
}

int main() {
    std::vector<ParticipationSystem> systems = {
        {"P001", 0.34, 0.22, 0.40, 0.24, 0.28, 0.42, 0.20, 0.18, 0.24},
        {"P004", 0.86, 0.84, 0.82, 0.80, 0.86, 0.84, 0.82, 0.86, 0.84},
        {"P008", 0.58, 0.24, 0.52, 0.18, 0.30, 0.54, 0.22, 0.16, 0.20}
    };

    std::sort(systems.begin(), systems.end(), [](const ParticipationSystem& a, const ParticipationSystem& b) {
        return participation_quality(a) > participation_quality(b);
    });

    for (const auto& s : systems) {
        std::cout << s.id
                  << " | quality " << participation_quality(s)
                  << " | tokenism risk " << tokenism_risk(s) << "\n";
    }

    return 0;
}
