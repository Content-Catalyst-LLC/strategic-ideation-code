// Efficient decision profile scoring example.
// Compile: g++ decision_uncertainty_score.cpp -std=c++17 -O2 -o decision_uncertainty_score
// Run: ./decision_uncertainty_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct OptionProfile {
    std::string name;
    double expected_return;
    double robustness;
    double flexibility;
    double information_quality;
    double exposure;
    double option_value;
    double reversibility;
    double ethical_resilience;
    double learning_value;
};

double decision_profile(const OptionProfile& o) {
    return 0.14 * o.expected_return +
           0.18 * o.robustness +
           0.16 * o.flexibility +
           0.12 * o.information_quality -
           0.16 * o.exposure +
           0.14 * o.option_value +
           0.10 * o.reversibility +
           0.10 * o.ethical_resilience +
           0.10 * o.learning_value;
}

double fragility_risk(const OptionProfile& o) {
    return 0.24 * o.exposure +
           0.18 * (1.0 - o.robustness) +
           0.14 * (1.0 - o.flexibility) +
           0.13 * (1.0 - o.option_value) +
           0.12 * (1.0 - o.reversibility) +
           0.10 * (1.0 - o.ethical_resilience) +
           0.09 * (1.0 - o.information_quality);
}

int main() {
    std::vector<OptionProfile> options = {
        {"High-Return Brittle Option", 0.86, 0.28, 0.31, 0.63, 0.82, 0.26, 0.22, 0.38, 0.30},
        {"Balanced Robust Option", 0.72, 0.79, 0.74, 0.72, 0.44, 0.72, 0.68, 0.68, 0.70},
        {"Exploratory Optionality Option", 0.61, 0.71, 0.88, 0.49, 0.53, 0.86, 0.82, 0.62, 0.88}
    };

    std::sort(options.begin(), options.end(), [](const OptionProfile& a, const OptionProfile& b) {
        return decision_profile(a) > decision_profile(b);
    });

    for (const auto& option : options) {
        std::cout << option.name
                  << " | profile " << decision_profile(option)
                  << " | fragility " << fragility_risk(option) << "\n";
    }

    return 0;
}
