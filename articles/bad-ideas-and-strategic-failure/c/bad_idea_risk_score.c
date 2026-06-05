#include <stdio.h>

typedef struct {
    const char *name;
    double frame, mechanism, evidence, implementation, incentive, ethics, support, merit, learning;
} BadIdea;

double max0(double value) {
    return value > 0.0 ? value : 0.0;
}

double risk(BadIdea i) {
    double distortion = max0(i.support - i.merit);
    return 0.14*(1-i.frame) + 0.12*(1-i.mechanism) + 0.15*(1-i.evidence) +
           0.14*(1-i.implementation) + 0.12*(1-i.incentive) + 0.12*(1-i.ethics) +
           0.11*(1-i.learning) + 0.10*distortion;
}

int main(void) {
    BadIdea ideas[] = {
        {"AI-Assisted Workflow Redesign", 0.54, 0.56, 0.52, 0.48, 0.44, 0.46, 0.78, 0.58, 0.46},
        {"Cost Consolidation Plan", 0.50, 0.52, 0.48, 0.44, 0.36, 0.38, 0.82, 0.54, 0.40},
        {"Reversible Pilot Portfolio", 0.74, 0.72, 0.70, 0.72, 0.68, 0.70, 0.58, 0.78, 0.82}
    };

    int count = sizeof(ideas) / sizeof(ideas[0]);
    for (int i = 0; i < count; i++) {
        printf("%s | bad-idea risk %.3f\n", ideas[i].name, risk(ideas[i]));
    }
    return 0;
}
