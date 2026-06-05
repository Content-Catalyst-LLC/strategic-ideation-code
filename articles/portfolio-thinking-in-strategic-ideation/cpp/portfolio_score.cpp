// Efficient strategic portfolio scoring example.
// Compile: g++ portfolio_score.cpp -std=c++17 -O2 -o portfolio_score
// Run: ./portfolio_score

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct IdeaProfile {
    std::string name;
    double impact;
    double risk;
    double learning;
    double option_value;
    double strategic_fit;
    double capacity_demand;
    double ethical_resilience;
};

double contribution(const IdeaProfile& i) {
    return 0.18 * i.impact +
           0.18 * i.strategic_fit +
           0.16 * i.learning +
           0.16 * i.option_value +
           0.14 * i.ethical_resilience -
           0.10 * i.risk -
           0.08 * i.capacity_demand;
}

double overload(const IdeaProfile& i) {
    return 0.34 * i.capacity_demand +
           0.24 * i.risk +
           0.16 * (1.0 - i.strategic_fit) +
           0.14 * (1.0 - i.ethical_resilience) +
           0.12 * (1.0 - i.option_value);
}

int main() {
    std::vector<IdeaProfile> ideas = {
        {"Core Process Improvement", 0.68, 0.32, 0.38, 0.34, 0.72, 0.44, 0.58},
        {"Exploratory Market Experiment", 0.58, 0.56, 0.84, 0.76, 0.62, 0.38, 0.62},
        {"Transformational Strategic Bet", 0.88, 0.78, 0.70, 0.62, 0.70, 0.86, 0.48}
    };

    std::sort(ideas.begin(), ideas.end(), [](const IdeaProfile& a, const IdeaProfile& b) {
        return contribution(a) > contribution(b);
    });

    for (const auto& idea : ideas) {
        std::cout << idea.name
                  << " | contribution " << contribution(idea)
                  << " | overload warning " << overload(idea) << "\n";
    }

    return 0;
}
