// Efficient systems-ideation scoring example.
// Compile: g++ systems_score.cpp -std=c++17 -O2 -o systems_score
// Run: ./systems_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct SystemProfile {
    std::string id;
    double feedback;
    double leverage;
    double root_cause;
    double stakeholder;
    double boundary;
    double stock_flow;
    double delay;
    double learning;
    double consequence_risk;
    double local_risk;
};

double score(const SystemProfile& s) {
    return 0.14 * s.feedback
         + 0.14 * s.leverage
         + 0.13 * s.root_cause
         + 0.12 * s.stakeholder
         + 0.12 * s.boundary
         + 0.10 * s.stock_flow
         + 0.10 * s.delay
         + 0.13 * s.learning
         - 0.10 * s.consequence_risk
         - 0.08 * s.local_risk;
}

double symptom_focus_risk(const SystemProfile& s) {
    return (1.0 - s.root_cause) * 0.30
         + (1.0 - s.leverage) * 0.25
         + s.local_risk * 0.25
         + s.consequence_risk * 0.20;
}

int main() {
    std::vector<SystemProfile> systems = {
        {"SYS001", 0.24, 0.21, 0.31, 0.28, 0.34, 0.30, 0.26, 0.29, 0.79, 0.76},
        {"SYS003", 0.86, 0.91, 0.88, 0.70, 0.78, 0.82, 0.76, 0.83, 0.36, 0.32},
        {"SYS005", 0.78, 0.76, 0.80, 0.90, 0.86, 0.74, 0.72, 0.82, 0.34, 0.30}
    };

    std::sort(systems.begin(), systems.end(), [](const SystemProfile& a, const SystemProfile& b) {
        return score(a) > score(b);
    });

    for (const auto& system : systems) {
        std::cout << system.id << " | score " << score(system)
                  << " | symptom risk " << symptom_focus_risk(system) << "\n";
    }

    return 0;
}
