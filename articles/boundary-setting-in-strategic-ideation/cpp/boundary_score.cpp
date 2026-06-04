// Efficient boundary quality scoring example.
// Compile: g++ boundary_score.cpp -std=c++17 -O2 -o boundary_score
// Run: ./boundary_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Boundary {
    std::string id;
    double problem;
    double system;
    double stakeholder;
    double causal;
    double temporal;
    double institutional;
    double evidence;
    double ethical;
    double revision;
    double actionability;
};

double boundary_quality(const Boundary& b) {
    return 0.12 * b.problem
         + 0.13 * b.system
         + 0.14 * b.stakeholder
         + 0.14 * b.causal
         + 0.12 * b.temporal
         + 0.11 * b.institutional
         + 0.11 * b.evidence
         + 0.10 * b.ethical
         + 0.09 * b.revision
         + 0.04 * b.actionability;
}

int main() {
    std::vector<Boundary> boundaries = {
        {"B001", 0.62, 0.38, 0.34, 0.42, 0.38, 0.50, 0.40, 0.32, 0.38, 0.82},
        {"B003", 0.82, 0.90, 0.72, 0.88, 0.76, 0.78, 0.74, 0.70, 0.72, 0.58},
        {"B005", 0.84, 0.86, 0.82, 0.82, 0.84, 0.80, 0.86, 0.84, 0.90, 0.66}
    };

    std::sort(boundaries.begin(), boundaries.end(), [](const Boundary& a, const Boundary& b) {
        return boundary_quality(a) > boundary_quality(b);
    });

    for (const auto& boundary : boundaries) {
        std::cout << boundary.id << " | boundary quality " << boundary_quality(boundary) << "\n";
    }

    return 0;
}
