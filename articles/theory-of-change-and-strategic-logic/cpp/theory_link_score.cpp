// Efficient theory-of-change link risk scoring example.
// Compile: g++ theory_link_score.cpp -std=c++17 -O2 -o theory_link_score
// Run: ./theory_link_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Link {
    std::string id;
    double mechanism_clarity;
    double evidence_strength;
    double actor_dependency;
    double capacity_dependency;
    double system_dependency;
    double ethical_dependency;
    double failure_consequence;
    double testability;
};

double link_risk(const Link& l) {
    return 0.16 * (1.0 - l.mechanism_clarity)
         + 0.18 * (1.0 - l.evidence_strength)
         + 0.13 * l.actor_dependency
         + 0.11 * l.capacity_dependency
         + 0.14 * l.system_dependency
         + 0.12 * l.ethical_dependency
         + 0.16 * l.failure_consequence;
}

double test_priority(const Link& l) {
    return link_risk(l) * l.testability;
}

int main() {
    std::vector<Link> links = {
        {"L002", 0.66, 0.38, 0.86, 0.62, 0.58, 0.52, 0.80, 0.78},
        {"L004", 0.72, 0.44, 0.82, 0.58, 0.68, 0.90, 0.86, 0.74},
        {"L009", 0.48, 0.32, 0.62, 0.48, 0.64, 0.60, 0.78, 0.58}
    };

    std::sort(links.begin(), links.end(), [](const Link& a, const Link& b) {
        return link_risk(a) > link_risk(b);
    });

    for (const auto& link : links) {
        std::cout << link.id
                  << " | link risk " << link_risk(link)
                  << " | test priority " << test_priority(link) << "\n";
    }

    return 0;
}
