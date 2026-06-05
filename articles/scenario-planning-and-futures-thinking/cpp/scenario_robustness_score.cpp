// Efficient scenario robustness scoring example.
// Compile: g++ scenario_robustness_score.cpp -std=c++17 -O2 -o scenario_robustness_score
// Run: ./scenario_robustness_score

#include <algorithm>
#include <cmath>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    std::vector<double> scenario_values;
    double flexibility;
    double implementation_readiness;
    double ethical_resilience;
    double option_value;
};

double mean(const std::vector<double>& values) {
    return std::accumulate(values.begin(), values.end(), 0.0) / values.size();
}

double stddev(const std::vector<double>& values) {
    double m = mean(values);
    double sum = 0.0;
    for (double v : values) {
        sum += (v - m) * (v - m);
    }
    return std::sqrt(sum / values.size());
}

double worst_case(const std::vector<double>& values) {
    return *std::min_element(values.begin(), values.end());
}

double robustness_profile(const Strategy& s) {
    return 0.30 * worst_case(s.scenario_values) +
           0.24 * mean(s.scenario_values) +
           0.16 * s.flexibility +
           0.12 * s.implementation_readiness +
           0.10 * s.ethical_resilience +
           0.10 * s.option_value -
           0.12 * stddev(s.scenario_values);
}

int main() {
    std::vector<Strategy> strategies = {
        {"Short-Term Optimization Strategy", {0.84, 0.41, 0.36, 0.48, 0.38}, 0.28, 0.86, 0.42, 0.30},
        {"Balanced Adaptive Strategy", {0.74, 0.71, 0.67, 0.70, 0.66}, 0.73, 0.74, 0.68, 0.72},
        {"Resilience-Oriented Strategy", {0.68, 0.75, 0.79, 0.73, 0.76}, 0.82, 0.66, 0.76, 0.78}
    };

    std::sort(strategies.begin(), strategies.end(), [](const Strategy& a, const Strategy& b) {
        return robustness_profile(a) > robustness_profile(b);
    });

    for (const auto& s : strategies) {
        std::cout << s.name
                  << " | mean " << mean(s.scenario_values)
                  << " | worst " << worst_case(s.scenario_values)
                  << " | robustness " << robustness_profile(s) << "\n";
    }

    return 0;
}
