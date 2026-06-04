// Efficient analogical transfer scoring example.
// Compile: g++ analogical_score.cpp -std=c++17 -O2 -o analogical_score
// Run: ./analogical_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string id;
    double structural;
    double functional;
    double surface;
    double adaptation;
    double context;
    double legitimacy;
    double dynamic;
    double innovation;
    double evidence;
};

double score(const Strategy& s) {
    return 0.20 * s.structural
         + 0.16 * s.functional
         - 0.16 * s.surface
         + 0.16 * s.adaptation
         + 0.12 * s.context
         + 0.08 * s.legitimacy
         + 0.08 * s.dynamic
         + 0.12 * s.innovation
         + 0.08 * s.evidence;
}

int main() {
    std::vector<Strategy> strategies = {
        {"A001", 0.28, 0.46, 0.82, 0.34, 0.30, 0.38, 0.26, 0.29, 0.36},
        {"A005", 0.89, 0.83, 0.22, 0.86, 0.84, 0.78, 0.86, 0.88, 0.80},
        {"A007", 0.82, 0.78, 0.34, 0.80, 0.76, 0.82, 0.84, 0.78, 0.76}
    };

    std::sort(strategies.begin(), strategies.end(), [](const Strategy& a, const Strategy& b) {
        return score(a) > score(b);
    });

    for (const auto& strategy : strategies) {
        std::cout << strategy.id << " | " << score(strategy) << "\n";
    }

    return 0;
}
