#include <stdio.h>

typedef struct {
    const char *name;
    double voice, evidence, burden, uncertainty, reversibility, long_term, ai, accountability, redress;
} EthicalIdea;

double legitimacy(EthicalIdea i) {
    return 0.14*i.voice + 0.14*i.evidence + 0.12*i.burden + 0.11*i.uncertainty +
           0.10*i.reversibility + 0.13*i.long_term + 0.08*i.ai + 0.10*i.accountability + 0.08*i.redress;
}

int main(void) {
    EthicalIdea ideas[] = {
        {"AI-Assisted Service Triage", 0.42, 0.56, 0.44, 0.46, 0.50, 0.52, 0.38, 0.48, 0.36},
        {"Participatory Governance Council", 0.84, 0.72, 0.78, 0.70, 0.72, 0.74, 0.62, 0.76, 0.72},
        {"Workforce Restructuring Plan", 0.38, 0.58, 0.40, 0.44, 0.36, 0.42, 0.40, 0.46, 0.34}
    };

    int count = sizeof(ideas) / sizeof(ideas[0]);
    for (int i = 0; i < count; i++) {
        double value = legitimacy(ideas[i]);
        printf("%s | ethical legitimacy %.3f | ethical risk %.3f\n", ideas[i].name, value, 1.0 - value);
    }
    return 0;
}
