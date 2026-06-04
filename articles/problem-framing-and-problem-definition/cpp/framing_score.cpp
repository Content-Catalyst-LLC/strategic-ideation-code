// Efficient problem-framing scoring example.
// Compile: g++ framing_score.cpp -std=c++17 -O2 -o framing_score
// Run: ./framing_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Frame {
    std::string id;
    double boundary;
    double stakeholder;
    double systems;
    double causal;
    double assumptions;
    double reframing;
    double actionability;
    double lock_in;
    double politics;
};

double score(const Frame& f) {
    return 0.16 * f.boundary
         + 0.15 * f.stakeholder
         + 0.15 * f.systems
         + 0.16 * f.causal
         + 0.12 * f.assumptions
         + 0.13 * f.reframing
         + 0.11 * f.actionability
         - 0.10 * f.lock_in
         - 0.08 * f.politics;
}

double symptom_risk(const Frame& f) {
    double boundary_gap = std::max(0.0, 0.70 - f.boundary);
    return (1.0 - f.causal) * 0.30
         + (1.0 - f.systems) * 0.25
         + boundary_gap * 0.20
         + f.lock_in * 0.15
         + f.politics * 0.10;
}

int main() {
    std::vector<Frame> frames = {
        {"F001", 0.28, 0.34, 0.26, 0.31, 0.24, 0.22, 0.62, 0.82, 0.70},
        {"F003", 0.86, 0.79, 0.91, 0.84, 0.78, 0.82, 0.72, 0.32, 0.34},
        {"F005", 0.82, 0.92, 0.78, 0.74, 0.76, 0.80, 0.74, 0.34, 0.30}
    };

    std::sort(frames.begin(), frames.end(), [](const Frame& a, const Frame& b) {
        return score(a) > score(b);
    });

    for (const auto& frame : frames) {
        std::cout << frame.id << " | score " << score(frame)
                  << " | symptom risk " << symptom_risk(frame) << "\n";
    }

    return 0;
}
