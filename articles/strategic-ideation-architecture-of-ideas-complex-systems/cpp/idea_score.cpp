#include <iostream>
#include <vector>

double weighted_score(const std::vector<double>& values, const std::vector<double>& weights) {
    double score = 0.0;

    for (size_t i = 0; i < values.size(); ++i) {
        score += values[i] * weights[i];
    }

    return score;
}

int main() {
    std::vector<double> values = {0.62, 0.86, 0.68, 0.88, 0.74, 0.35, 0.63};
    std::vector<double> weights = {0.16, 0.20, 0.16, 0.20, 0.14, -0.08, 0.14};

    std::cout << "Synthetic strategic idea score: " << weighted_score(values, weights) << "\n";

    return 0;
}
