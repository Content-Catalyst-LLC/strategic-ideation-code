// Efficient layer portfolio scoring example.
// Compile: g++ layer_portfolio_scoring.cpp -std=c++17 -O2 -o layer_portfolio_scoring
// Run: ./layer_portfolio_scoring

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Initiative {
    std::string id;
    double strategic_fit;
    double feasibility;
    double systems_leverage;
    double learning_value;
    double ethics;
    double uncertainty;
};

double score(const Initiative& item) {
    return 0.22 * item.strategic_fit
         + 0.14 * item.feasibility
         + 0.18 * item.systems_leverage
         + 0.14 * item.learning_value
         + 0.18 * item.ethics
         - 0.08 * item.uncertainty;
}

int main() {
    std::vector<Initiative> items = {
        {"S001", 0.89, 0.76, 0.78, 0.91, 0.84, 0.24},
        {"S004", 0.88, 0.68, 0.82, 0.94, 0.86, 0.31},
        {"S010", 0.87, 0.58, 0.86, 0.92, 0.88, 0.43}
    };

    std::sort(items.begin(), items.end(), [](const Initiative& a, const Initiative& b) {
        return score(a) > score(b);
    });

    for (const auto& item : items) {
        std::cout << item.id << " | " << score(item) << "\n";
    }

    return 0;
}
