// Efficient strategic narrative coherence scoring example.
// Compile: g++ narrative_score.cpp -std=c++17 -O2 -o narrative_score
// Run: ./narrative_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Narrative {
    std::string id;
    double diagnosis;
    double purpose;
    double choice;
    double sequence;
    double role;
    double future;
    double accountability;
    double evidence;
    double stakeholder;
    double ethics;
};

double score(const Narrative& n) {
    return 0.14 * n.diagnosis
         + 0.12 * n.purpose
         + 0.14 * n.choice
         + 0.12 * n.sequence
         + 0.11 * n.role
         + 0.10 * n.future
         + 0.11 * n.accountability
         + 0.08 * n.evidence
         + 0.05 * n.stakeholder
         + 0.03 * n.ethics;
}

int main() {
    std::vector<Narrative> narratives = {
        {"SN001", 0.32, 0.44, 0.28, 0.30, 0.36, 0.42, 0.25, 0.34, 0.38, 0.35},
        {"SN003", 0.86, 0.82, 0.76, 0.84, 0.78, 0.80, 0.82, 0.84, 0.78, 0.81},
        {"SN006", 0.72, 0.80, 0.69, 0.67, 0.76, 0.78, 0.73, 0.76, 0.91, 0.89}
    };

    std::sort(narratives.begin(), narratives.end(), [](const Narrative& a, const Narrative& b) {
        return score(a) > score(b);
    });

    for (const auto& narrative : narratives) {
        std::cout << narrative.id << " | " << score(narrative) << "\n";
    }

    return 0;
}
