// Efficient strategic hypothesis scoring example.
// Compile: g++ hypothesis_score.cpp -std=c++17 -O2 -o hypothesis_score
// Run: ./hypothesis_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Hypothesis {
    std::string id;
    double explanatory;
    double testability;
    double evidence;
    double relevance;
    double stakeholder;
    double systems;
    double actionability;
    double risk;
    double reversibility;
};

double score(const Hypothesis& h) {
    return 0.16 * h.explanatory
         + 0.14 * h.testability
         + 0.14 * h.evidence
         + 0.16 * h.relevance
         + 0.12 * h.stakeholder
         + 0.12 * h.systems
         + 0.10 * h.actionability
         + 0.06 * h.reversibility
         - 0.10 * h.risk;
}

int main() {
    std::vector<Hypothesis> hypotheses = {
        {"H001", 0.82, 0.74, 0.68, 0.86, 0.72, 0.76, 0.72, 0.52, 0.74},
        {"H004", 0.84, 0.70, 0.66, 0.86, 0.92, 0.78, 0.64, 0.58, 0.66},
        {"H010", 0.88, 0.68, 0.72, 0.90, 0.66, 0.86, 0.62, 0.66, 0.58}
    };

    std::sort(hypotheses.begin(), hypotheses.end(), [](const Hypothesis& a, const Hypothesis& b) {
        return score(a) > score(b);
    });

    for (const auto& hypothesis : hypotheses) {
        std::cout << hypothesis.id << " | " << score(hypothesis) << "\n";
    }

    return 0;
}
