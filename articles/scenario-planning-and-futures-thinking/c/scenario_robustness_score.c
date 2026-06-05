/*
Low-level scenario robustness score utilities.
Compile: cc scenario_robustness_score.c -lm -o scenario_robustness_score
Run: ./scenario_robustness_score
*/

#include <math.h>
#include <stdio.h>

typedef struct {
    const char *name;
    double values[5];
    double flexibility;
    double implementation_readiness;
    double ethical_resilience;
    double option_value;
} Strategy;

double mean(double values[], int count) {
    double total = 0.0;
    for (int i = 0; i < count; i++) {
        total += values[i];
    }
    return total / count;
}

double worst(double values[], int count) {
    double w = 1.0;
    for (int i = 0; i < count; i++) {
        if (values[i] < w) {
            w = values[i];
        }
    }
    return w;
}

double stddev(double values[], int count) {
    double m = mean(values, count);
    double total = 0.0;
    for (int i = 0; i < count; i++) {
        total += (values[i] - m) * (values[i] - m);
    }
    return sqrt(total / count);
}

double robustness_profile(Strategy s) {
    return 0.30 * worst(s.values, 5) +
           0.24 * mean(s.values, 5) +
           0.16 * s.flexibility +
           0.12 * s.implementation_readiness +
           0.10 * s.ethical_resilience +
           0.10 * s.option_value -
           0.12 * stddev(s.values, 5);
}

int main(void) {
    Strategy strategies[] = {
        {"Short-Term Optimization Strategy", {0.84, 0.41, 0.36, 0.48, 0.38}, 0.28, 0.86, 0.42, 0.30},
        {"Balanced Adaptive Strategy", {0.74, 0.71, 0.67, 0.70, 0.66}, 0.73, 0.74, 0.68, 0.72},
        {"Resilience-Oriented Strategy", {0.68, 0.75, 0.79, 0.73, 0.76}, 0.82, 0.66, 0.76, 0.78}
    };

    int count = sizeof(strategies) / sizeof(strategies[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | mean %.3f | worst %.3f | robustness %.3f\n",
               strategies[i].name,
               mean(strategies[i].values, 5),
               worst(strategies[i].values, 5),
               robustness_profile(strategies[i]));
    }

    return 0;
}
