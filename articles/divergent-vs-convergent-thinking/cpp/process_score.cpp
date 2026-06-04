// Efficient divergence-convergence process scoring example.
// Compile: g++ process_score.cpp -std=c++17 -O2 -o process_score
// Run: ./process_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Context {
    std::string id;
    double exploration;
    double evaluation;
    double iteration;
    double constraints;
    double inclusion;
    double evidence;
    double readiness;
    double memory;
};

double score(const Context& c) {
    return 0.16 * c.exploration
         + 0.16 * c.evaluation
         + 0.18 * c.iteration
         + 0.14 * c.constraints
         + 0.12 * c.inclusion
         + 0.12 * c.evidence
         + 0.08 * c.readiness
         + 0.04 * c.memory;
}

int main() {
    std::vector<Context> contexts = {
        {"DC001", 0.28, 0.86, 0.31, 0.71, 0.34, 0.42, 0.79, 0.38},
        {"DC002", 0.74, 0.77, 0.76, 0.73, 0.70, 0.74, 0.81, 0.72},
        {"DC004", 0.79, 0.72, 0.88, 0.69, 0.76, 0.82, 0.77, 0.80}
    };

    std::sort(contexts.begin(), contexts.end(), [](const Context& a, const Context& b) {
        return score(a) > score(b);
    });

    for (const auto& context : contexts) {
        std::cout << context.id << " | " << score(context) << "\n";
    }

    return 0;
}
