// Efficient second-order effects scoring example.
// Compile: g++ second_order_score.cpp -std=c++17 -O2 -o second_order_score
// Run: ./second_order_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Intervention {
    std::string id;
    double first_gain;
    double adaptation;
    double feedback;
    double delay;
    double burden;
    double gaming;
    double fragility;
    double learning;
    double legitimacy;
    double reversibility;
};

double second_order_risk(const Intervention& i) {
    return 0.16 * i.adaptation
         + 0.15 * i.feedback
         + 0.14 * i.delay
         + 0.15 * i.burden
         + 0.14 * i.gaming
         + 0.16 * i.fragility
         - 0.10 * i.learning
         - 0.06 * i.legitimacy
         - 0.06 * i.reversibility;
}

double false_success_risk(const Intervention& i) {
    return 0.26 * i.first_gain
         + 0.20 * i.fragility
         + 0.16 * i.delay
         + 0.14 * i.gaming
         + 0.12 * i.burden
         - 0.16 * i.learning;
}

int main() {
    std::vector<Intervention> interventions = {
        {"I001", 0.88, 0.76, 0.58, 0.69, 0.66, 0.52, 0.82, 0.38, 0.44, 0.42},
        {"I002", 0.71, 0.44, 0.51, 0.42, 0.34, 0.28, 0.39, 0.76, 0.72, 0.70},
        {"I003", 0.63, 0.81, 0.73, 0.57, 0.78, 0.74, 0.74, 0.42, 0.46, 0.38}
    };

    std::sort(interventions.begin(), interventions.end(), [](const Intervention& a, const Intervention& b) {
        return second_order_risk(a) > second_order_risk(b);
    });

    for (const auto& intervention : interventions) {
        std::cout << intervention.id
                  << " | second-order risk " << second_order_risk(intervention)
                  << " | false-success risk " << false_success_risk(intervention) << "\n";
    }

    return 0;
}
