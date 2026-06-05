// Efficient knowledge architecture scoring example.
// Compile: g++ knowledge_architecture_score.cpp -std=c++17 -O2 -o knowledge_architecture_score
// Run: ./knowledge_architecture_score

#include <iostream>
#include <string>
#include <vector>

struct Idea {
    std::string name;
    double taxonomy, metadata, semantics, evidence, assumptions, relationships, retrieval, memory, stewardship, ethics;
};

double score(const Idea& i) {
    return 0.11*i.taxonomy + 0.12*i.metadata + 0.11*i.semantics + 0.12*i.evidence +
           0.11*i.assumptions + 0.11*i.relationships + 0.12*i.retrieval +
           0.09*i.memory + 0.07*i.stewardship + 0.04*i.ethics;
}

int main() {
    std::vector<Idea> ideas = {
        {"Community Data Stewardship", 0.74, 0.70, 0.76, 0.66, 0.68, 0.72, 0.70, 0.62, 0.64, 0.78},
        {"AI-Assisted Scenario Library", 0.62, 0.58, 0.54, 0.52, 0.50, 0.58, 0.54, 0.46, 0.48, 0.46},
        {"Strategic Learning Repository", 0.78, 0.80, 0.82, 0.74, 0.72, 0.82, 0.84, 0.78, 0.76, 0.66}
    };
    for (const auto& i : ideas) {
        double value = score(i);
        std::cout << i.name << " | architecture strength " << value << " | risk " << 1.0 - value << "\n";
    }
    return 0;
}
