/*
Low-level adaptive strategy scoring utilities.
Compile: cc adaptive_strategy_score.c -o adaptive_strategy_score
Run: ./adaptive_strategy_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double flexibility;
    double learning_capacity;
    double exploration;
    double exploitation_balance;
    double coherence;
    double feedback_intelligence;
    double governance;
    double systems_awareness;
    double learning_memory;
} Strategy;

double adaptive_score(Strategy s) {
    return 0.13 * s.flexibility +
           0.15 * s.learning_capacity +
           0.09 * s.exploration +
           0.11 * s.exploitation_balance +
           0.15 * s.coherence +
           0.13 * s.feedback_intelligence +
           0.10 * s.governance +
           0.08 * s.systems_awareness +
           0.06 * s.learning_memory;
}

double over_adaptation_risk(Strategy s) {
    return 0.20 * s.flexibility * (1.0 - s.coherence) +
           0.18 * (1.0 - s.governance) +
           0.16 * (1.0 - s.feedback_intelligence) +
           0.14 * (1.0 - s.learning_capacity) +
           0.12 * (1.0 - s.exploitation_balance) +
           0.10 * (1.0 - s.learning_memory) +
           0.10 * (1.0 - s.systems_awareness);
}

int main(void) {
    Strategy strategies[] = {
        {"AS001", 0.24, 0.31, 0.18, 0.74, 0.81, 0.34, 0.62, 0.38, 0.36},
        {"AS002", 0.82, 0.84, 0.68, 0.79, 0.76, 0.82, 0.78, 0.74, 0.76},
        {"AS004", 0.86, 0.49, 0.57, 0.32, 0.28, 0.42, 0.24, 0.36, 0.30}
    };

    int count = sizeof(strategies) / sizeof(strategies[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | adaptive score %.3f | over-adaptation risk %.3f\n",
               strategies[i].id,
               adaptive_score(strategies[i]),
               over_adaptation_risk(strategies[i]));
    }

    return 0;
}
