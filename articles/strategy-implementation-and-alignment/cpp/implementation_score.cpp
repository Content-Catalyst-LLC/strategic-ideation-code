// Efficient implementation profile scoring example.
// Compile: g++ implementation_score.cpp -std=c++17 -O2 -o implementation_score
// Run: ./implementation_score

#include <iostream>
#include <string>
#include <vector>

struct Profile {
    std::string name;
    double goal, coordination, structure, culture, incentives, resources, communication, accountability, adaptation;
};

double score(const Profile& p) {
    return 0.12*p.goal + 0.15*p.coordination + 0.12*p.structure + 0.12*p.culture +
           0.13*p.incentives + 0.12*p.resources + 0.11*p.communication + 0.10*p.accountability + 0.10*p.adaptation;
}

int main() {
    std::vector<Profile> profiles = {
        {"High-Intent Fragmented Organization", 0.70, 0.38, 0.44, 0.31, 0.29, 0.52, 0.41, 0.46, 0.36},
        {"Balanced Aligned Organization", 0.82, 0.81, 0.79, 0.78, 0.77, 0.82, 0.80, 0.76, 0.74},
        {"Adaptive Cross-Functional Organization", 0.78, 0.84, 0.73, 0.76, 0.71, 0.76, 0.78, 0.74, 0.83}
    };
    for (const auto& p : profiles) std::cout << p.name << " | implementation score " << score(p) << "\n";
    return 0;
}
