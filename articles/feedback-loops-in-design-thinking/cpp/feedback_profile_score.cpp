// Efficient feedback profile scoring example.
// Compile: g++ feedback_profile_score.cpp -std=c++17 -O2 -o feedback_profile_score
// Run: ./feedback_profile_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct FeedbackSystem {
    std::string id;
    double signal_quality;
    double interpretation_capacity;
    double adjustment_speed;
    double user_insight_depth;
    double stability;
    double ethical_integrity;
    double systems_awareness;
    double decision_linkage;
    double learning_memory;
};

double feedback_profile(const FeedbackSystem& s) {
    return 0.13 * s.signal_quality +
           0.13 * s.interpretation_capacity +
           0.10 * s.adjustment_speed +
           0.13 * s.user_insight_depth +
           0.10 * s.stability +
           0.11 * s.ethical_integrity +
           0.10 * s.systems_awareness +
           0.10 * s.decision_linkage +
           0.10 * s.learning_memory;
}

double noisy_churn_risk(const FeedbackSystem& s) {
    return 0.16 * s.adjustment_speed +
           0.15 * (1.0 - s.signal_quality) +
           0.15 * (1.0 - s.interpretation_capacity) +
           0.13 * (1.0 - s.stability) +
           0.12 * (1.0 - s.systems_awareness) +
           0.12 * (1.0 - s.ethical_integrity) +
           0.10 * (1.0 - s.decision_linkage) +
           0.07 * (1.0 - s.learning_memory);
}

int main() {
    std::vector<FeedbackSystem> systems = {
        {"F001", 0.34, 0.31, 0.29, 0.36, 0.41, 0.38, 0.32, 0.28, 0.26},
        {"F004", 0.82, 0.84, 0.63, 0.88, 0.72, 0.72, 0.84, 0.80, 0.82},
        {"F006", 0.62, 0.42, 0.34, 0.46, 0.50, 0.40, 0.38, 0.24, 0.28}
    };

    std::sort(systems.begin(), systems.end(), [](const FeedbackSystem& a, const FeedbackSystem& b) {
        return feedback_profile(a) > feedback_profile(b);
    });

    for (const auto& s : systems) {
        std::cout << s.id
                  << " | profile " << feedback_profile(s)
                  << " | noisy churn risk " << noisy_churn_risk(s) << "\n";
    }

    return 0;
}
