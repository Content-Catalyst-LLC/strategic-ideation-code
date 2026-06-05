// Efficient strategic tradeoff scoring example.
// Compile: g++ risk_tradeoff_score.cpp -std=c++17 -O2 -o risk_tradeoff_score
// Run: ./risk_tradeoff_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct OptionProfile {
    std::string name;
    double short_term_return;
    double resilience;
    double flexibility;
    double legitimacy;
    double opportunity_value;
    double exposure;
    double reversibility;
    double ethical_resilience;
    double learning_value;
};

double tradeoff_score(const OptionProfile& o) {
    return 0.18 * o.short_term_return +
           0.20 * o.resilience +
           0.16 * o.flexibility +
           0.14 * o.legitimacy +
           0.14 * o.opportunity_value -
           0.18 * o.exposure +
           0.08 * o.reversibility +
           0.08 * o.ethical_resilience +
           0.08 * o.learning_value;
}

double fragility_warning(const OptionProfile& o) {
    return 0.26 * o.exposure +
           0.18 * (1.0 - o.resilience) +
           0.14 * (1.0 - o.flexibility) +
           0.12 * (1.0 - o.legitimacy) +
           0.12 * (1.0 - o.opportunity_value) +
           0.10 * (1.0 - o.reversibility) +
           0.08 * (1.0 - o.ethical_resilience);
}

int main() {
    std::vector<OptionProfile> options = {
        {"Efficiency-Optimized Option", 0.86, 0.32, 0.36, 0.48, 0.34, 0.74, 0.30, 0.42, 0.34},
        {"Balanced Strategic Option", 0.71, 0.74, 0.76, 0.72, 0.70, 0.46, 0.68, 0.70, 0.72},
        {"Resilience-First Option", 0.58, 0.88, 0.79, 0.81, 0.76, 0.34, 0.72, 0.82, 0.70}
    };

    std::sort(options.begin(), options.end(), [](const OptionProfile& a, const OptionProfile& b) {
        return tradeoff_score(a) > tradeoff_score(b);
    });

    for (const auto& option : options) {
        std::cout << option.name
                  << " | tradeoff score " << tradeoff_score(option)
                  << " | fragility warning " << fragility_warning(option) << "\n";
    }

    return 0;
}
