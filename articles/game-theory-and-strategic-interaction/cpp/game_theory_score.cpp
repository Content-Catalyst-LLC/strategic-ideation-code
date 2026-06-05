// Efficient strategic interaction scoring example.
// Compile: g++ game_theory_score.cpp -std=c++17 -O2 -o game_theory_score
// Run: ./game_theory_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Setting {
    std::string name;
    double rivalry;
    double coordination;
    double information_asymmetry;
    double retaliation;
    double institutional_support;
    double behavioral_realism;
    double mechanism_design;
    double ethical_complexity;
};

double mechanism_opportunity(const Setting& s) {
    return 0.30 * s.mechanism_design +
           0.18 * s.coordination +
           0.16 * s.information_asymmetry +
           0.14 * s.ethical_complexity +
           0.12 * s.institutional_support +
           0.10 * s.behavioral_realism;
}

double cooperation_fragility(const Setting& s) {
    return 0.22 * s.rivalry +
           0.20 * s.retaliation +
           0.16 * s.information_asymmetry +
           0.12 * s.ethical_complexity -
           0.15 * s.institutional_support -
           0.15 * s.coordination;
}

int main() {
    std::vector<Setting> settings = {
        {"Price Competition Environment", 0.84, 0.28, 0.44, 0.76, 0.39, 0.52, 0.42, 0.46},
        {"Standards Coordination Environment", 0.36, 0.86, 0.31, 0.24, 0.73, 0.68, 0.78, 0.54},
        {"Platform Ecosystem Environment", 0.71, 0.74, 0.69, 0.58, 0.57, 0.74, 0.82, 0.76}
    };

    std::sort(settings.begin(), settings.end(), [](const Setting& a, const Setting& b) {
        return mechanism_opportunity(a) > mechanism_opportunity(b);
    });

    for (const auto& s : settings) {
        std::cout << s.name
                  << " | mechanism opportunity " << mechanism_opportunity(s)
                  << " | cooperation fragility " << cooperation_fragility(s) << "\n";
    }

    return 0;
}
