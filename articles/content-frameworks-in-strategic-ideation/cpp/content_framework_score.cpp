// Efficient content framework scoring example.
// Compile: g++ content_framework_score.cpp -std=c++17 -O2 -o content_framework_score
// Run: ./content_framework_score

#include <iostream>
#include <string>
#include <vector>

struct Framework {
    std::string name;
    double structure, clarity, evidence, assumptions, narrative, decision, modularity, reuse, governance, ethics;
};

double score(const Framework& f) {
    return 0.11*f.structure + 0.11*f.clarity + 0.12*f.evidence + 0.10*f.assumptions +
           0.10*f.narrative + 0.13*f.decision + 0.10*f.modularity +
           0.10*f.reuse + 0.08*f.governance + 0.05*f.ethics;
}

int main() {
    std::vector<Framework> frameworks = {
        {"Idea Record Framework", 0.76, 0.72, 0.66, 0.68, 0.62, 0.64, 0.74, 0.72, 0.66, 0.60},
        {"Decision Memo Framework", 0.82, 0.76, 0.80, 0.78, 0.74, 0.86, 0.66, 0.68, 0.72, 0.72},
        {"AI-Assisted Ideation Framework", 0.62, 0.56, 0.50, 0.48, 0.58, 0.54, 0.60, 0.58, 0.46, 0.42}
    };
    for (const auto& f : frameworks) {
        double value = score(f);
        std::cout << f.name << " | framework strength " << value << " | risk " << 1.0 - value << "\n";
    }
    return 0;
}
