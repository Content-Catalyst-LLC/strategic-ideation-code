/*
Low-level experimentation profile scoring utilities.
Compile: cc experiment_profile_score.c -o experiment_profile_score
Run: ./experiment_profile_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double speed;
    double cost_efficiency;
    double insight_depth;
    double user_validation;
    double assumption_criticality;
    double evidence_quality;
    double systems_awareness;
    double ethical_review;
    double decision_linkage;
    double learning_memory;
} System;

double experimentation_profile(System s) {
    return 0.10 * s.speed +
           0.09 * s.cost_efficiency +
           0.15 * s.insight_depth +
           0.12 * s.user_validation +
           0.12 * s.assumption_criticality +
           0.14 * s.evidence_quality +
           0.10 * s.systems_awareness +
           0.08 * s.ethical_review +
           0.10 * s.decision_linkage +
           0.10 * s.learning_memory;
}

double superficial_testing_risk(System s) {
    return 0.14 * s.speed +
           0.16 * (1.0 - s.insight_depth) +
           0.15 * (1.0 - s.evidence_quality) +
           0.13 * (1.0 - s.systems_awareness) +
           0.13 * (1.0 - s.ethical_review) +
           0.13 * (1.0 - s.decision_linkage) +
           0.09 * (1.0 - s.assumption_criticality) +
           0.07 * (1.0 - s.learning_memory);
}

int main(void) {
    System systems[] = {
        {"E001", 0.24, 0.31, 0.42, 0.36, 0.44, 0.38, 0.34, 0.42, 0.30, 0.32},
        {"E004", 0.61, 0.67, 0.89, 0.84, 0.86, 0.88, 0.82, 0.70, 0.82, 0.80},
        {"E006", 0.70, 0.50, 0.36, 0.42, 0.38, 0.34, 0.28, 0.30, 0.24, 0.22}
    };

    int count = sizeof(systems) / sizeof(systems[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | profile %.3f | superficial testing risk %.3f\n",
               systems[i].id,
               experimentation_profile(systems[i]),
               superficial_testing_risk(systems[i]));
    }

    return 0;
}
