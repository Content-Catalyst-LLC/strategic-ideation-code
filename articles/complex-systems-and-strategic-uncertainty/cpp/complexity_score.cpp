// Efficient complexity profile scoring example.
// Compile: g++ complexity_score.cpp -std=c++17 -O2 -o complexity_score
// Run: ./complexity_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Environment {
    std::string id;
    double interdependence;
    double nonlinearity;
    double feedback;
    double adaptation;
    double path;
    double boundary;
    double emergence;
    double deep_uncertainty;
    double scenario_need;
    double learning_need;
};

double complexity_score(const Environment& e) {
    return 0.13 * e.interdependence
         + 0.13 * e.nonlinearity
         + 0.14 * e.feedback
         + 0.12 * e.adaptation
         + 0.11 * e.path
         + 0.10 * e.boundary
         + 0.10 * e.emergence
         + 0.09 * e.deep_uncertainty
         + 0.09 * e.scenario_need
         + 0.09 * e.learning_need;
}

double linear_planning_risk(const Environment& e) {
    return 0.20 * e.nonlinearity
         + 0.20 * e.feedback
         + 0.18 * e.adaptation
         + 0.16 * e.deep_uncertainty
         + 0.14 * e.boundary
         + 0.12 * e.emergence;
}

int main() {
    std::vector<Environment> environments = {
        {"ENV001", 0.32, 0.24, 0.31, 0.28, 0.36, 0.30, 0.26, 0.28, 0.30, 0.34},
        {"ENV003", 0.81, 0.74, 0.79, 0.71, 0.78, 0.76, 0.74, 0.82, 0.82, 0.80},
        {"ENV004", 0.88, 0.86, 0.87, 0.82, 0.84, 0.82, 0.86, 0.90, 0.90, 0.88}
    };

    std::sort(environments.begin(), environments.end(), [](const Environment& a, const Environment& b) {
        return complexity_score(a) > complexity_score(b);
    });

    for (const auto& environment : environments) {
        std::cout << environment.id << " | complexity " << complexity_score(environment)
                  << " | linear planning risk " << linear_planning_risk(environment) << "\n";
    }

    return 0;
}
