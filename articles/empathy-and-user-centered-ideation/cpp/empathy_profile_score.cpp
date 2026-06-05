// Efficient empathy profile scoring example.
// Compile: g++ empathy_profile_score.cpp -std=c++17 -O2 -o empathy_profile_score
// Run: ./empathy_profile_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Context {
    std::string id;
    double observation;
    double projection;
    double unmet_need;
    double stakeholder_breadth;
    double reframing;
    double ethics;
    double systems;
    double decision;
    double memory;
};

double empathy_profile(const Context& c) {
    return 0.16 * c.observation
         - 0.14 * c.projection
         + 0.16 * c.unmet_need
         + 0.12 * c.stakeholder_breadth
         + 0.16 * c.reframing
         + 0.10 * c.ethics
         + 0.10 * c.systems
         + 0.14 * c.decision
         + 0.10 * c.memory;
}

double superficiality_risk(const Context& c) {
    return 0.20 * c.projection
         + 0.16 * (1.0 - c.decision)
         + 0.14 * (1.0 - c.observation)
         + 0.12 * (1.0 - c.unmet_need)
         + 0.12 * (1.0 - c.ethics)
         + 0.10 * (1.0 - c.systems)
         + 0.08 * (1.0 - c.stakeholder_breadth)
         + 0.08 * (1.0 - c.memory);
}

int main() {
    std::vector<Context> contexts = {
        {"C001", 0.24, 0.84, 0.31, 0.28, 0.34, 0.38, 0.35, 0.32, 0.30},
        {"C004", 0.76, 0.48, 0.79, 0.90, 0.83, 0.86, 0.88, 0.78, 0.76},
        {"C005", 0.38, 0.72, 0.42, 0.36, 0.40, 0.32, 0.30, 0.24, 0.22}
    };

    std::sort(contexts.begin(), contexts.end(), [](const Context& a, const Context& b) {
        return empathy_profile(a) > empathy_profile(b);
    });

    for (const auto& c : contexts) {
        std::cout << c.id
                  << " | empathy profile " << empathy_profile(c)
                  << " | superficiality risk " << superficiality_risk(c) << "\n";
    }

    return 0;
}
