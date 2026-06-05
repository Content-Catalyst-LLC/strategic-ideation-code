// Efficient strategic effectiveness scoring example.
// Compile: g++ effectiveness_score.cpp -std=c++17 -O2 -o effectiveness_score
// Run: ./effectiveness_score

#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double performance, alignment, resilience, adaptability, impact, learning, confidence, ethics;
};

double score(const Strategy& s) {
    return 0.20*s.performance + 0.15*s.alignment + 0.16*s.resilience + 0.15*s.adaptability +
           0.14*s.impact + 0.10*s.learning + 0.05*s.confidence + 0.05*s.ethics;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Efficiency-Led Strategy", 0.84, 0.58, 0.42, 0.46, 0.51, 0.42, 0.66, 0.48},
        {"Balanced Capability Strategy", 0.72, 0.79, 0.76, 0.78, 0.73, 0.76, 0.74, 0.72},
        {"Adaptive Learning Strategy", 0.70, 0.76, 0.78, 0.88, 0.74, 0.90, 0.70, 0.76}
    };
    for (const auto& s : strategies) {
        double value = score(s);
        std::cout << s.name << " | score " << value << " | confidence-adjusted " << value * s.confidence << "\n";
    }
    return 0;
}
