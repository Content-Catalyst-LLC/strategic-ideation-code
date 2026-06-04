// Efficient mental-model profile scoring example.
// Compile: g++ model_profile_scoring.cpp -std=c++17 -O2 -o model_profile_scoring
// Run: ./model_profile_scoring

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Model {
    std::string id;
    double systems;
    double probability;
    double flexibility;
    double plurality;
    double revision;
    double embedding;
    double ethics;
    double stakeholder;
    double evidence;
};

double adaptive_score(const Model& m) {
    return 0.17 * m.systems
         + 0.13 * m.probability
         + 0.16 * m.flexibility
         + 0.14 * m.plurality
         + 0.16 * m.revision
         - 0.08 * m.embedding
         + 0.12 * m.ethics
         + 0.10 * m.stakeholder
         + 0.10 * m.evidence;
}

int main() {
    std::vector<Model> models = {
        {"M001", 0.24, 0.21, 0.19, 0.22, 0.22, 0.58, 0.31, 0.28, 0.34},
        {"M003", 0.89, 0.84, 0.88, 0.86, 0.87, 0.71, 0.82, 0.80, 0.86},
        {"M010", 0.82, 0.67, 0.78, 0.84, 0.79, 0.52, 0.93, 0.94, 0.78}
    };

    std::sort(models.begin(), models.end(), [](const Model& a, const Model& b) {
        return adaptive_score(a) > adaptive_score(b);
    });

    for (const auto& model : models) {
        std::cout << model.id << " | " << adaptive_score(model) << "\n";
    }

    return 0;
}
