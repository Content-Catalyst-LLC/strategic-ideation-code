// Efficient strategic creativity scoring example.
// Compile: g++ creativity_score.cpp -std=c++17 -O2 -o creativity_score
// Run: ./creativity_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Idea {
    std::string id;
    double novelty;
    double relevance;
    double coherence;
    double mechanism;
    double testability;
    double stakeholder;
    double systems;
    double development;
    double risk;
    double revision;
};

double score(const Idea& i) {
    return 0.14 * i.novelty
         + 0.16 * i.relevance
         + 0.13 * i.coherence
         + 0.14 * i.mechanism
         + 0.11 * i.testability
         + 0.13 * i.stakeholder
         + 0.13 * i.systems
         + 0.12 * i.development
         + 0.08 * i.revision
         - 0.12 * i.risk;
}

double novelty_theater_risk(const Idea& i) {
    return i.novelty * (1.0 - ((i.mechanism + i.stakeholder + i.systems) / 3.0));
}

int main() {
    std::vector<Idea> ideas = {
        {"I002", 0.72, 0.86, 0.78, 0.80, 0.70, 0.92, 0.78, 0.82, 0.56, 0.82},
        {"I005", 0.76, 0.88, 0.82, 0.84, 0.66, 0.70, 0.90, 0.86, 0.66, 0.86},
        {"I009", 0.70, 0.50, 0.52, 0.34, 0.46, 0.30, 0.32, 0.42, 0.40, 0.38}
    };

    std::sort(ideas.begin(), ideas.end(), [](const Idea& a, const Idea& b) {
        return score(a) > score(b);
    });

    for (const auto& idea : ideas) {
        std::cout << idea.id << " | " << score(idea) << " | novelty risk " << novelty_theater_risk(idea) << "\n";
    }

    return 0;
}
