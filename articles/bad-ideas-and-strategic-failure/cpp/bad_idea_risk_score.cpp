// Efficient bad-idea risk scoring example.
// Compile: g++ bad_idea_risk_score.cpp -std=c++17 -O2 -o bad_idea_risk_score
// Run: ./bad_idea_risk_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct BadIdea {
    std::string name;
    double frame, mechanism, evidence, implementation, incentive, ethics, support, merit, learning;
};

double risk(const BadIdea& i) {
    double distortion = std::max(0.0, i.support - i.merit);
    return 0.14*(1-i.frame) + 0.12*(1-i.mechanism) + 0.15*(1-i.evidence) +
           0.14*(1-i.implementation) + 0.12*(1-i.incentive) + 0.12*(1-i.ethics) +
           0.11*(1-i.learning) + 0.10*distortion;
}

int main() {
    std::vector<BadIdea> ideas = {
        {"AI-Assisted Workflow Redesign", 0.54, 0.56, 0.52, 0.48, 0.44, 0.46, 0.78, 0.58, 0.46},
        {"Cost Consolidation Plan", 0.50, 0.52, 0.48, 0.44, 0.36, 0.38, 0.82, 0.54, 0.40},
        {"Reversible Pilot Portfolio", 0.74, 0.72, 0.70, 0.72, 0.68, 0.70, 0.58, 0.78, 0.82}
    };

    for (const auto& i : ideas) {
        std::cout << i.name << " | bad-idea risk " << risk(i) << "\n";
    }
    return 0;
}
