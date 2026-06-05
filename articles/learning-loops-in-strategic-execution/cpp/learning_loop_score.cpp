// Efficient learning loop scoring example.
// Compile: g++ learning_loop_score.cpp -std=c++17 -O2 -o learning_loop_score
// Run: ./learning_loop_score

#include <iostream>
#include <string>
#include <vector>

struct Context {
    std::string name;
    double feedback, assumptions, interpretation, authority, closure, memory, safety, scaling, ethics;
};

double score(const Context& c) {
    return 0.13*c.feedback + 0.13*c.assumptions + 0.12*c.interpretation +
           0.14*c.authority + 0.14*c.closure + 0.10*c.memory +
           0.09*c.safety + 0.08*c.scaling + 0.07*c.ethics;
}

int main() {
    std::vector<Context> contexts = {
        {"Reporting-Heavy Organization", 0.62, 0.42, 0.46, 0.38, 0.34, 0.36, 0.44, 0.40, 0.50},
        {"Adaptive Learning Organization", 0.84, 0.82, 0.80, 0.78, 0.82, 0.76, 0.78, 0.74, 0.80},
        {"Pilot-Rich Memory-Poor Organization", 0.72, 0.60, 0.62, 0.56, 0.48, 0.30, 0.58, 0.36, 0.56}
    };
    for (const auto& c : contexts) {
        double value = score(c);
        std::cout << c.name << " | learning loop strength " << value << " | learning debt " << 1.0 - value << "\n";
    }
    return 0;
}
