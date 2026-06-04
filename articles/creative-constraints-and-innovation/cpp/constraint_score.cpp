// Efficient creative constraint profile scoring example.
// Compile: g++ constraint_score.cpp -std=c++17 -O2 -o constraint_score
// Run: ./constraint_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Context {
    std::string id;
    double resource;
    double technical;
    double institutional;
    double ecological;
    double ethics;
    double focus;
    double opportunity;
    double legitimacy;
    double learning;
    double readiness;
};

double score(const Context& c) {
    return -0.10 * c.resource
         - 0.10 * c.technical
         - 0.10 * c.institutional
         + 0.12 * c.ecological
         + 0.16 * c.ethics
         + 0.16 * c.focus
         + 0.16 * c.opportunity
         + 0.14 * c.legitimacy
         + 0.14 * c.learning
         + 0.12 * c.readiness;
}

int main() {
    std::vector<Context> contexts = {
        {"CC001", 0.12, 0.18, 0.16, 0.20, 0.38, 0.24, 0.38, 0.42, 0.36, 0.34},
        {"CC002", 0.54, 0.47, 0.43, 0.52, 0.66, 0.78, 0.81, 0.72, 0.78, 0.76},
        {"CC007", 0.66, 0.52, 0.57, 0.92, 0.88, 0.74, 0.70, 0.82, 0.76, 0.60}
    };

    std::sort(contexts.begin(), contexts.end(), [](const Context& a, const Context& b) {
        return score(a) > score(b);
    });

    for (const auto& context : contexts) {
        std::cout << context.id << " | " << score(context) << "\n";
    }

    return 0;
}
