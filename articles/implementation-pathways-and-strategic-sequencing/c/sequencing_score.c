#include <stdio.h>

typedef struct {
    const char *name;
    double capability, evidence, governance, legitimacy, dependency, reversibility, capacity, timing, ethics;
} Pathway;

double score(Pathway p) {
    return 0.16*p.capability + 0.15*p.evidence + 0.15*p.governance + 0.14*p.legitimacy -
           0.12*p.dependency + 0.10*p.reversibility - 0.10*p.capacity + 0.08*p.timing + 0.12*p.ethics;
}

int main(void) {
    Pathway pathways[] = {
        {"Data Governance Foundation", 0.72, 0.66, 0.78, 0.62, 0.42, 0.70, 0.46, 0.52, 0.70},
        {"Full Platform Rollout", 0.52, 0.46, 0.48, 0.44, 0.82, 0.38, 0.84, 0.60, 0.42},
        {"Adaptive Rollout Sequence", 0.70, 0.68, 0.72, 0.74, 0.52, 0.76, 0.60, 0.66, 0.78}
    };
    int count = sizeof(pathways) / sizeof(pathways[0]);
    for (int i = 0; i < count; i++) {
        printf("%s | sequencing readiness %.3f\n", pathways[i].name, score(pathways[i]));
    }
    return 0;
}
