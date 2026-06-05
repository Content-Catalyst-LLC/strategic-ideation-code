// Efficient institutional power scoring example.
// Compile: g++ power_distortion_score.cpp -std=c++17 -O2 -o power_distortion_score
// Run: ./power_distortion_score

#include <iostream>
#include <string>
#include <vector>

struct PowerIdea {
    std::string name;
    double merit, evidence, sponsorship, resource_fit, stakeholder, dissent, classification, power_alignment, advancement;
};

double merit_score(const PowerIdea& i) {
    return 0.32*i.merit + 0.24*i.evidence + 0.18*i.stakeholder + 0.14*i.dissent + 0.12*i.classification;
}

double support_score(const PowerIdea& i) {
    return 0.30*i.sponsorship + 0.25*i.resource_fit + 0.25*i.power_alignment + 0.20*i.advancement;
}

int main() {
    std::vector<PowerIdea> ideas = {
        {"Participatory Governance Model", 0.78, 0.72, 0.54, 0.58, 0.78, 0.72, 0.76, 0.46, 0.52},
        {"Executive Dashboard Expansion", 0.62, 0.60, 0.86, 0.82, 0.42, 0.46, 0.58, 0.84, 0.82},
        {"Cost Consolidation Plan", 0.58, 0.52, 0.82, 0.80, 0.34, 0.38, 0.46, 0.86, 0.80}
    };
    for (const auto& i : ideas) {
        double merit = merit_score(i);
        double support = support_score(i);
        std::cout << i.name << " | merit " << merit << " | institutional support " << support << " | power distortion " << support - merit << "\n";
    }
    return 0;
}
