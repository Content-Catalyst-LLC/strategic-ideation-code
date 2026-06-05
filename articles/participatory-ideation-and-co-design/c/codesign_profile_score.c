/*
Low-level co-design profile scoring utilities.
Compile: cc codesign_profile_score.c -o codesign_profile_score
Run: ./codesign_profile_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double representation;
    double influence;
    double accessibility;
    double reciprocity;
    double power_awareness;
    double knowledge_integration;
    double decision_linkage;
    double accountability;
    double learning_memory;
} ParticipationSystem;

double participation_quality(ParticipationSystem s) {
    return 0.13 * s.representation +
           0.15 * s.influence +
           0.11 * s.accessibility +
           0.11 * s.reciprocity +
           0.13 * s.power_awareness +
           0.12 * s.knowledge_integration +
           0.11 * s.decision_linkage +
           0.10 * s.accountability +
           0.04 * s.learning_memory;
}

double tokenism_risk(ParticipationSystem s) {
    return 0.16 * (1.0 - s.influence) +
           0.14 * (1.0 - s.decision_linkage) +
           0.14 * (1.0 - s.accountability) +
           0.13 * (1.0 - s.reciprocity) +
           0.13 * (1.0 - s.power_awareness) +
           0.11 * (1.0 - s.representation) +
           0.10 * (1.0 - s.accessibility) +
           0.09 * (1.0 - s.learning_memory);
}

int main(void) {
    ParticipationSystem systems[] = {
        {"P001", 0.34, 0.22, 0.40, 0.24, 0.28, 0.42, 0.20, 0.18, 0.24},
        {"P004", 0.86, 0.84, 0.82, 0.80, 0.86, 0.84, 0.82, 0.86, 0.84},
        {"P008", 0.58, 0.24, 0.52, 0.18, 0.30, 0.54, 0.22, 0.16, 0.20}
    };

    int count = sizeof(systems) / sizeof(systems[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | quality %.3f | tokenism risk %.3f\n",
               systems[i].id,
               participation_quality(systems[i]),
               tokenism_risk(systems[i]));
    }

    return 0;
}
