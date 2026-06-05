/*
Low-level prototype evidence scoring utilities.
Compile: cc prototype_evidence_score.c -o prototype_evidence_score
Run: ./prototype_evidence_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double assumption_clarity;
    double learning_target_fit;
    double evidence_quality;
    double behavioral_grounding;
    double context_realism;
    double systems_awareness;
    double decision_linkage;
    double ethical_review;
    double learning_memory;
} PrototypeSystem;

double learning_quality(PrototypeSystem s) {
    return 0.13 * s.assumption_clarity +
           0.13 * s.learning_target_fit +
           0.15 * s.evidence_quality +
           0.13 * s.behavioral_grounding +
           0.11 * s.context_realism +
           0.11 * s.systems_awareness +
           0.11 * s.decision_linkage +
           0.07 * s.ethical_review +
           0.06 * s.learning_memory;
}

double validation_theater_risk(PrototypeSystem s) {
    return 0.17 * (1.0 - s.assumption_clarity) +
           0.16 * (1.0 - s.evidence_quality) +
           0.14 * (1.0 - s.behavioral_grounding) +
           0.13 * (1.0 - s.decision_linkage) +
           0.12 * (1.0 - s.learning_memory) +
           0.11 * (1.0 - s.systems_awareness) +
           0.09 * (1.0 - s.ethical_review) +
           0.08 * (1.0 - s.context_realism);
}

int main(void) {
    PrototypeSystem systems[] = {
        {"PE001", 0.30, 0.28, 0.26, 0.22, 0.34, 0.24, 0.20, 0.28, 0.22},
        {"PE004", 0.84, 0.82, 0.84, 0.76, 0.80, 0.88, 0.82, 0.72, 0.82},
        {"PE007", 0.52, 0.46, 0.40, 0.26, 0.32, 0.30, 0.38, 0.36, 0.34}
    };

    int count = sizeof(systems) / sizeof(systems[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | learning quality %.3f | validation theater risk %.3f\n",
               systems[i].id,
               learning_quality(systems[i]),
               validation_theater_risk(systems[i]));
    }

    return 0;
}
