// Efficient idea portfolio scoring example.
// Compile: g++ idea_portfolio_scoring.cpp -std=c++17 -O2 -o idea_portfolio_scoring
// Run: ./idea_portfolio_scoring

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Idea {
    std::string id;
    double strategic_fit;
    double feasibility;
    double systems_leverage;
    double learning_value;
    double ethical_legitimacy;
    double knowledge_reusability;
    double uncertainty;
    double assumption_risk;
};

double score(const Idea& idea) {
    return 0.20 * idea.strategic_fit
         + 0.12 * idea.feasibility
         + 0.18 * idea.systems_leverage
         + 0.13 * idea.learning_value
         + 0.16 * idea.ethical_legitimacy
         + 0.09 * idea.knowledge_reusability
         - 0.07 * idea.uncertainty
         - 0.05 * idea.assumption_risk;
}

int main() {
    std::vector<Idea> ideas = {
        {"I001", 0.91, 0.82, 0.74, 0.88, 0.86, 0.94, 0.24, 0.29},
        {"I010", 0.90, 0.73, 0.80, 0.87, 0.84, 0.88, 0.29, 0.33},
        {"I012", 0.85, 0.64, 0.84, 0.94, 0.88, 0.85, 0.39, 0.44}
    };

    std::sort(ideas.begin(), ideas.end(), [](const Idea& a, const Idea& b) {
        return score(a) > score(b);
    });

    for (const auto& idea : ideas) {
        std::cout << idea.id << " | " << score(idea) << "\n";
    }

    return 0;
}
