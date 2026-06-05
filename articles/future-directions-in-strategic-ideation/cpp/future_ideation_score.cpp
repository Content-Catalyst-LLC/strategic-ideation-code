// Efficient future-ready strategic ideation scoring example.
// Compile: g++ future_ideation_score.cpp -std=c++17 -O2 -o future_ideation_score
// Run: ./future_ideation_score

#include <iostream>
#include <string>
#include <vector>

struct FutureIdea {
    std::string name;
    double frame, evidence, adaptability, scenario, stakeholder, implementation, ethics, learning, option_value, ai;
};

double future_ready_score(const FutureIdea& i) {
    return 0.11*i.frame + 0.11*i.evidence + 0.11*i.adaptability + 0.12*i.scenario +
           0.11*i.stakeholder + 0.10*i.implementation + 0.11*i.ethics + 0.12*i.learning +
           0.07*i.option_value + 0.04*i.ai;
}

int main() {
    std::vector<FutureIdea> ideas = {
        {"Scenario-Linked Option Portfolio", 0.78, 0.72, 0.84, 0.86, 0.70, 0.70, 0.76, 0.86, 0.90, 0.62},
        {"Participatory Strategy Lab", 0.80, 0.74, 0.78, 0.72, 0.86, 0.64, 0.84, 0.78, 0.72, 0.56},
        {"Rapid Automation Initiative", 0.54, 0.52, 0.48, 0.46, 0.42, 0.50, 0.44, 0.42, 0.46, 0.38}
    };

    for (const auto& i : ideas) {
        double score = future_ready_score(i);
        std::cout << i.name << " | future-ready score " << score << " | future risk " << 1.0 - score << "\n";
    }
    return 0;
}
