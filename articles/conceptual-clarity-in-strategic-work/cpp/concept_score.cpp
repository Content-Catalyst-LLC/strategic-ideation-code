// Efficient conceptual clarity scoring example.
// Compile: g++ concept_score.cpp -std=c++17 -O2 -o concept_score
// Run: ./concept_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Concept {
    std::string id;
    double definition;
    double boundary;
    double distinction;
    double operational;
    double measurement;
    double revision;
    double stakeholder;
    double ethics;
    double governance;
};

double score(const Concept& c) {
    return 0.17 * c.definition
         + 0.14 * c.boundary
         + 0.14 * c.distinction
         + 0.13 * c.operational
         + 0.15 * c.measurement
         + 0.10 * c.revision
         + 0.07 * c.stakeholder
         + 0.06 * c.ethics
         + 0.04 * c.governance;
}

int main() {
    std::vector<Concept> concepts = {
        {"CC001", 0.42, 0.31, 0.44, 0.52, 0.36, 0.29, 0.46, 0.41, 0.30},
        {"CC003", 0.64, 0.55, 0.68, 0.70, 0.60, 0.52, 0.66, 0.71, 0.50},
        {"CC006", 0.58, 0.50, 0.61, 0.63, 0.54, 0.49, 0.68, 0.78, 0.47}
    };

    std::sort(concepts.begin(), concepts.end(), [](const Concept& a, const Concept& b) {
        return score(a) > score(b);
    });

    for (const auto& concept : concepts) {
        std::cout << concept.id << " | " << score(concept) << "\n";
    }

    return 0;
}
