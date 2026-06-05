/*
Low-level feedback profile scoring utilities.
Compile: cc feedback_profile_score.c -o feedback_profile_score
Run: ./feedback_profile_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double signal_quality;
    double interpretation_capacity;
    double adjustment_speed;
    double user_insight_depth;
    double stability;
    double ethical_integrity;
    double systems_awareness;
    double decision_linkage;
    double learning_memory;
} FeedbackSystem;

double feedback_profile(FeedbackSystem s) {
    return 0.13 * s.signal_quality +
           0.13 * s.interpretation_capacity +
           0.10 * s.adjustment_speed +
           0.13 * s.user_insight_depth +
           0.10 * s.stability +
           0.11 * s.ethical_integrity +
           0.10 * s.systems_awareness +
           0.10 * s.decision_linkage +
           0.10 * s.learning_memory;
}

double noisy_churn_risk(FeedbackSystem s) {
    return 0.16 * s.adjustment_speed +
           0.15 * (1.0 - s.signal_quality) +
           0.15 * (1.0 - s.interpretation_capacity) +
           0.13 * (1.0 - s.stability) +
           0.12 * (1.0 - s.systems_awareness) +
           0.12 * (1.0 - s.ethical_integrity) +
           0.10 * (1.0 - s.decision_linkage) +
           0.07 * (1.0 - s.learning_memory);
}

int main(void) {
    FeedbackSystem systems[] = {
        {"F001", 0.34, 0.31, 0.29, 0.36, 0.41, 0.38, 0.32, 0.28, 0.26},
        {"F004", 0.82, 0.84, 0.63, 0.88, 0.72, 0.72, 0.84, 0.80, 0.82},
        {"F006", 0.62, 0.42, 0.34, 0.46, 0.50, 0.40, 0.38, 0.24, 0.28}
    };

    int count = sizeof(systems) / sizeof(systems[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | profile %.3f | noisy churn risk %.3f\n",
               systems[i].id,
               feedback_profile(systems[i]),
               noisy_churn_risk(systems[i]));
    }

    return 0;
}
