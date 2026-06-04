// Efficient heuristic profile scoring example.
// Compile: g++ heuristic_score.cpp -std=c++17 -O2 -o heuristic_score
// Run: ./heuristic_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Context {
    std::string id;
    double availability;
    double anchoring;
    double recognition;
    double satisficing;
    double affect;
    double default_gravity;
    double social_proof;
    double diversity;
    double stakeholder;
    double source_domain;
    double systems;
    double political;
    double memory;
};

double score(const Context& c) {
    return -0.11 * c.availability
         - 0.11 * c.anchoring
         - 0.10 * c.recognition
         - 0.11 * c.satisficing
         - 0.07 * c.affect
         - 0.08 * c.default_gravity
         - 0.06 * c.social_proof
         + 0.17 * c.diversity
         + 0.13 * c.stakeholder
         + 0.13 * c.source_domain
         + 0.14 * c.systems
         + 0.07 * c.political
         + 0.08 * c.memory;
}

int main() {
    std::vector<Context> contexts = {
        {"H001", 0.84, 0.63, 0.79, 0.82, 0.66, 0.72, 0.70, 0.29, 0.34, 0.28, 0.40, 0.48, 0.34},
        {"H004", 0.31, 0.27, 0.36, 0.34, 0.32, 0.30, 0.28, 0.89, 0.82, 0.88, 0.78, 0.74, 0.72},
        {"H005", 0.76, 0.72, 0.82, 0.78, 0.62, 0.88, 0.74, 0.30, 0.28, 0.26, 0.36, 0.30, 0.36}
    };

    std::sort(contexts.begin(), contexts.end(), [](const Context& a, const Context& b) {
        return score(a) > score(b);
    });

    for (const auto& context : contexts) {
        std::cout << context.id << " | " << score(context) << "\n";
    }

    return 0;
}
