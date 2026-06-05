// Efficient institutional memory scoring example.
// Compile: g++ institutional_memory_score.cpp -std=c++17 -O2 -o institutional_memory_score
// Run: ./institutional_memory_score

#include <iostream>
#include <string>
#include <vector>

struct MemorySystem {
    std::string name;
    double capture, metadata, context, decisions, learning, retrieval, reuse, stewardship, continuity, ethics;
};

double score(const MemorySystem& m) {
    return 0.10*m.capture + 0.12*m.metadata + 0.12*m.context + 0.13*m.decisions +
           0.12*m.learning + 0.12*m.retrieval + 0.10*m.reuse +
           0.08*m.stewardship + 0.06*m.continuity + 0.05*m.ethics;
}

int main() {
    std::vector<MemorySystem> systems = {
        {"Strategic Idea Repository", 0.72, 0.80, 0.76, 0.66, 0.68, 0.78, 0.80, 0.72, 0.70, 0.62},
        {"Decision Memory", 0.70, 0.74, 0.82, 0.86, 0.72, 0.74, 0.76, 0.70, 0.72, 0.70},
        {"Retired Ideas Archive", 0.58, 0.54, 0.56, 0.58, 0.48, 0.52, 0.60, 0.50, 0.48, 0.58}
    };
    for (const auto& m : systems) {
        double value = score(m);
        std::cout << m.name << " | memory strength " << value << " | failure risk " << 1.0 - value << "\n";
    }
    return 0;
}
