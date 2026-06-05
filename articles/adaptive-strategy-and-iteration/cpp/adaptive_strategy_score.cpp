// Efficient adaptive strategy scoring example.
// Compile: g++ adaptive_strategy_score.cpp -std=c++17 -O2 -o adaptive_strategy_score
// Run: ./adaptive_strategy_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string id;
    double flexibility;
    double learning_capacity;
    double exploration;
    double exploitation_balance;
    double coherence;
    double feedback_intelligence;
    double governance;
    double systems_awareness;
    double learning_memory;
};

double adaptive_score(const Strategy& s) {
    return 0.13 * s.flexibility +
           0.15 * s.learning_capacity +
           0.09 * s.exploration +
           0.11 * s.exploitation_balance +
           0.15 * s.coherence +
           0.13 * s.feedback_intelligence +
           0.10 * s.governance +
           0.08 * s.systems_awareness +
           0.06 * s.learning_memory;
}

double over_adaptation_risk(const Strategy& s) {
    return 0.20 * s.flexibility * (1.0 - s.coherence) +
           0.18 * (1.0 - s.governance) +
           0.16 * (1.0 - s.feedback_intelligence) +
           0.14 * (1.0 - s.learning_capacity) +
           0.12 * (1.0 - s.exploitation_balance) +
           0.10 * (1.0 - s.learning_memory) +
           0.10 * (1.0 - s.systems_awareness);
}

int main() {
    std::vector<Strategy> strategies = {
        {"AS001", 0.24, 0.31, 0.18, 0.74, 0.81, 0.34, 0.62, 0.38, 0.36},
        {"AS002", 0.82, 0.84, 0.68, 0.79, 0.76, 0.82, 0.78, 0.74, 0.76},
        {"AS004", 0.86, 0.49, 0.57, 0.32, 0.28, 0.42, 0.24, 0.36, 0.30}
    };

    std::sort(strategies.begin(), strategies.end(), [](const Strategy& a, const Strategy& b) {
        return adaptive_score(a) > adaptive_score(b);
    });

    for (const auto& s : strategies) {
        std::cout << s.id
                  << " | adaptive score " << adaptive_score(s)
                  << " | over-adaptation risk " << over_adaptation_risk(s) << "\n";
    }

    return 0;
}
