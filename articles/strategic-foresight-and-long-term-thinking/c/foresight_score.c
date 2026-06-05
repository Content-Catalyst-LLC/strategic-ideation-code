/*
Low-level strategic foresight score utilities.
Compile: cc foresight_score.c -o foresight_score
Run: ./foresight_score
*/

#include <stdio.h>

typedef struct {
    const char *name;
    double short_term_return;
    double foresight_depth;
    double resilience;
    double flexibility;
    double path_dependence_risk;
    double signal_capacity;
    double scenario_capacity;
    double option_value;
    double ethics_review;
    double governance_capacity;
} Strategy;

double future_viability(Strategy s) {
    return 0.18 * s.foresight_depth +
           0.18 * s.resilience +
           0.16 * s.flexibility +
           0.14 * s.option_value +
           0.12 * s.scenario_capacity +
           0.10 * s.signal_capacity +
           0.08 * s.governance_capacity +
           0.08 * s.ethics_review -
           0.14 * s.path_dependence_risk;
}

double short_term_bias(Strategy s) {
    return s.short_term_return - ((s.foresight_depth + s.resilience + s.flexibility + s.option_value) / 4.0);
}

int main(void) {
    Strategy strategies[] = {
        {"Short-Term Efficiency Strategy", 0.86, 0.24, 0.32, 0.28, 0.71, 0.30, 0.26, 0.30, 0.34, 0.42},
        {"Balanced Foresight Strategy", 0.72, 0.79, 0.76, 0.74, 0.39, 0.76, 0.74, 0.72, 0.68, 0.74},
        {"Resilience-Biased Long-Horizon Strategy", 0.61, 0.84, 0.88, 0.79, 0.34, 0.80, 0.82, 0.78, 0.76, 0.80}
    };

    int count = sizeof(strategies) / sizeof(strategies[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | future viability %.3f | short-term bias %.3f\n",
               strategies[i].name,
               future_viability(strategies[i]),
               short_term_bias(strategies[i]));
    }

    return 0;
}
