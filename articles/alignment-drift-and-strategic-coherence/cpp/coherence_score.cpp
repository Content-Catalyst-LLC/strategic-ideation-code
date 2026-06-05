// Efficient strategic coherence scoring example.
// Compile: g++ coherence_score.cpp -std=c++17 -O2 -o coherence_score
// Run: ./coherence_score

#include <iostream>
#include <string>
#include <vector>

struct Context {
    std::string name;
    double purpose, priority, tradeoff, resources, incentives, interpretation, governance, feedback, memory, ethics;
};

double score(const Context& c) {
    return 0.15*c.purpose + 0.12*c.priority + 0.11*c.tradeoff + 0.13*c.resources +
           0.13*c.incentives + 0.11*c.interpretation + 0.12*c.governance +
           0.08*c.feedback + 0.07*c.memory + 0.08*c.ethics;
}

int main() {
    std::vector<Context> contexts = {
        {"Symbolically Aligned Organization", 0.64, 0.50, 0.46, 0.46, 0.42, 0.50, 0.44, 0.48, 0.40, 0.54},
        {"Coherent Adaptive Organization", 0.84, 0.80, 0.78, 0.78, 0.80, 0.82, 0.78, 0.84, 0.76, 0.80},
        {"Metric-Substituted Organization", 0.68, 0.60, 0.54, 0.62, 0.36, 0.58, 0.52, 0.44, 0.50, 0.46}
    };
    for (const auto& c : contexts) {
        double value = score(c);
        std::cout << c.name << " | coherence " << value << " | drift risk " << 1.0 - value << "\n";
    }
    return 0;
}
