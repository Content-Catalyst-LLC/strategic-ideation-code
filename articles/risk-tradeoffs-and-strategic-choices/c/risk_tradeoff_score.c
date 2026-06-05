/*
Low-level risk and tradeoff score utilities.
Compile: cc risk_tradeoff_score.c -o risk_tradeoff_score
Run: ./risk_tradeoff_score
*/

#include <stdio.h>

typedef struct {
    const char *name;
    double short_term_return;
    double resilience;
    double flexibility;
    double legitimacy;
    double opportunity_value;
    double exposure;
    double reversibility;
    double ethical_resilience;
    double learning_value;
} OptionProfile;

double tradeoff_score(OptionProfile o) {
    return 0.18 * o.short_term_return +
           0.20 * o.resilience +
           0.16 * o.flexibility +
           0.14 * o.legitimacy +
           0.14 * o.opportunity_value -
           0.18 * o.exposure +
           0.08 * o.reversibility +
           0.08 * o.ethical_resilience +
           0.08 * o.learning_value;
}

double fragility_warning(OptionProfile o) {
    return 0.26 * o.exposure +
           0.18 * (1.0 - o.resilience) +
           0.14 * (1.0 - o.flexibility) +
           0.12 * (1.0 - o.legitimacy) +
           0.12 * (1.0 - o.opportunity_value) +
           0.10 * (1.0 - o.reversibility) +
           0.08 * (1.0 - o.ethical_resilience);
}

int main(void) {
    OptionProfile options[] = {
        {"Efficiency-Optimized Option", 0.86, 0.32, 0.36, 0.48, 0.34, 0.74, 0.30, 0.42, 0.34},
        {"Balanced Strategic Option", 0.71, 0.74, 0.76, 0.72, 0.70, 0.46, 0.68, 0.70, 0.72},
        {"Resilience-First Option", 0.58, 0.88, 0.79, 0.81, 0.76, 0.34, 0.72, 0.82, 0.70}
    };

    int count = sizeof(options) / sizeof(options[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | tradeoff score %.3f | fragility warning %.3f\n",
               options[i].name,
               tradeoff_score(options[i]),
               fragility_warning(options[i]));
    }

    return 0;
}
