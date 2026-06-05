// Efficient taxonomy scoring example.
// Compile: g++ taxonomy_score.cpp -std=c++17 -O2 -o taxonomy_score
// Run: ./taxonomy_score

#include <iostream>
#include <string>
#include <vector>

struct TaxonomyRecord {
    std::string name;
    double category, level, maturity, evidence, function, relationships, retrieval, governance, ethics;
};

double score(const TaxonomyRecord& t) {
    return 0.13*t.category + 0.11*t.level + 0.11*t.maturity + 0.12*t.evidence +
           0.13*t.function + 0.11*t.relationships + 0.13*t.retrieval +
           0.09*t.governance + 0.07*t.ethics;
}

int main() {
    std::vector<TaxonomyRecord> records = {
        {"Strategic Learning Repository", 0.78, 0.76, 0.72, 0.72, 0.80, 0.76, 0.82, 0.74, 0.66},
        {"Participatory Governance Prototype", 0.76, 0.74, 0.76, 0.70, 0.74, 0.72, 0.76, 0.70, 0.82},
        {"Advisory Panel Without Authority", 0.66, 0.62, 0.72, 0.62, 0.60, 0.66, 0.62, 0.56, 0.76}
    };
    for (const auto& t : records) {
        double value = score(t);
        std::cout << t.name << " | taxonomy strength " << value << " | taxonomy risk " << 1.0 - value << "\n";
    }
    return 0;
}
