// Efficient scoring and portfolio example.
// Compile: g++ scoring.cpp -std=c++17 -O2 -o scoring
// Run: ./scoring

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
    double uncertainty;
};

double score(const Idea& idea) {
    return 0.28 * idea.strategic_fit
         + 0.18 * idea.feasibility
         + 0.24 * idea.systems_leverage
         + 0.18 * idea.learning_value
         - 0.12 * idea.uncertainty;
}

int main() {
    std::vector<Idea> ideas = {
        {"I001", 0.91, 0.82, 0.74, 0.88, 0.24},
        {"I004", 0.78, 0.76, 0.65, 0.95, 0.28},
        {"I008", 0.86, 0.70, 0.89, 0.88, 0.37}
    };

    std::sort(ideas.begin(), ideas.end(), [](const Idea& a, const Idea& b) {
        return score(a) > score(b);
    });

    for (const auto& idea : ideas) {
        std::cout << idea.id << " | " << score(idea) << "\n";
    }

    return 0;
}
