// Efficient lateral thinking profile scoring example.
// Compile: g++ lateral_score.cpp -std=c++17 -O2 -o lateral_score
// Run: ./lateral_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Context {
    std::string id;
    double rigidity;
    double provocation;
    double analogy;
    double random_entry;
    double reversal;
    double challenge;
    double convergence;
    double systems;
    double legitimacy;
    double political_safety;
    double transformation;
};

double score(const Context& c) {
    return -0.14 * c.rigidity
         + 0.14 * c.provocation
         + 0.12 * c.analogy
         + 0.09 * c.random_entry
         + 0.10 * c.reversal
         + 0.10 * c.challenge
         + 0.14 * c.convergence
         + 0.12 * c.systems
         + 0.08 * c.legitimacy
         + 0.07 * c.political_safety
         + 0.14 * c.transformation;
}

int main() {
    std::vector<Context> contexts = {
        {"LT001", 0.86, 0.18, 0.21, 0.16, 0.20, 0.28, 0.72, 0.44, 0.50, 0.48, 0.24},
        {"LT004", 0.36, 0.74, 0.76, 0.70, 0.78, 0.80, 0.82, 0.86, 0.78, 0.74, 0.88},
        {"LT008", 0.52, 0.78, 0.68, 0.72, 0.70, 0.46, 0.28, 0.34, 0.36, 0.40, 0.62}
    };

    std::sort(contexts.begin(), contexts.end(), [](const Context& a, const Context& b) {
        return score(a) > score(b);
    });

    for (const auto& context : contexts) {
        std::cout << context.id << " | " << score(context) << "\n";
    }

    return 0;
}
