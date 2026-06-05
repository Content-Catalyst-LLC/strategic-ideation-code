// Efficient journey profile scoring example.
// Compile: g++ journey_profile_score.cpp -std=c++17 -O2 -o journey_profile_score
// Run: ./journey_profile_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Journey {
    std::string id;
    double clarity;
    double emotional_confidence;
    double friction;
    double transition_quality;
    double accessibility;
    double trust;
    double completion_support;
    double backstage_alignment;
    double measurement_quality;
};

double journey_profile(const Journey& j) {
    return 0.15 * j.clarity +
           0.12 * j.emotional_confidence -
           0.18 * j.friction +
           0.14 * j.transition_quality +
           0.12 * j.accessibility +
           0.12 * j.trust +
           0.10 * j.completion_support +
           0.10 * j.backstage_alignment +
           0.07 * j.measurement_quality;
}

double redesign_need(const Journey& j) {
    return 0.22 * j.friction +
           0.16 * (1.0 - j.transition_quality) +
           0.14 * (1.0 - j.accessibility) +
           0.13 * (1.0 - j.trust) +
           0.12 * (1.0 - j.clarity) +
           0.11 * (1.0 - j.backstage_alignment) +
           0.07 * (1.0 - j.completion_support) +
           0.05 * (1.0 - j.measurement_quality);
}

int main() {
    std::vector<Journey> journeys = {
        {"J001", 0.36, 0.31, 0.82, 0.28, 0.34, 0.30, 0.34, 0.30, 0.38},
        {"J005", 0.81, 0.79, 0.28, 0.82, 0.88, 0.84, 0.86, 0.78, 0.76},
        {"J007", 0.54, 0.45, 0.72, 0.36, 0.50, 0.44, 0.52, 0.34, 0.46}
    };

    std::sort(journeys.begin(), journeys.end(), [](const Journey& a, const Journey& b) {
        return journey_profile(a) > journey_profile(b);
    });

    for (const auto& j : journeys) {
        std::cout << j.id
                  << " | journey profile " << journey_profile(j)
                  << " | redesign need " << redesign_need(j) << "\n";
    }

    return 0;
}
