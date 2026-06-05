#include <stdio.h>

typedef struct {
    const char *name;
    double concept, narrative, evidence, audience, decision, implementation, feedback, governance, ethics;
} Profile;

double score(Profile p) {
    return 0.12*p.concept + 0.12*p.narrative + 0.13*p.evidence + 0.10*p.audience +
           0.14*p.decision + 0.12*p.implementation + 0.08*p.feedback +
           0.10*p.governance + 0.09*p.ethics;
}

int main(void) {
    Profile profiles[] = {
        {"Executive Strategy Briefing", 0.74, 0.76, 0.72, 0.70, 0.82, 0.62, 0.58, 0.70, 0.64},
        {"Stakeholder Explanation", 0.68, 0.74, 0.70, 0.82, 0.66, 0.60, 0.78, 0.66, 0.84},
        {"AI-Assisted Message Set", 0.52, 0.58, 0.46, 0.60, 0.48, 0.46, 0.44, 0.42, 0.40}
    };
    int count = sizeof(profiles) / sizeof(profiles[0]);
    for (int i = 0; i < count; i++) {
        double value = score(profiles[i]);
        printf("%s | coherence strength %.3f | meaning loss risk %.3f\n", profiles[i].name, value, 1.0 - value);
    }
    return 0;
}
