/*
Low-level assumption score utilities.
Compile: cc assumption_score.c -o assumption_score
Run: ./assumption_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double criticality;
    double uncertainty;
    double evidence_strength;
    double evidence_relevance;
    double evidence_transferability;
    double testability;
    double stakeholder_sensitivity;
    double system_sensitivity;
} Assumption;

double evidence_composite(Assumption a) {
    return 0.40 * a.evidence_strength +
           0.30 * a.evidence_relevance +
           0.30 * a.evidence_transferability;
}

double evidence_adjusted_risk(Assumption a) {
    return a.criticality * a.uncertainty * (1.0 - evidence_composite(a));
}

double learning_value(Assumption a) {
    return 0.34 * evidence_adjusted_risk(a) +
           0.24 * a.testability +
           0.18 * a.stakeholder_sensitivity +
           0.14 * a.system_sensitivity +
           0.10 * a.criticality;
}

int main(void) {
    Assumption assumptions[] = {
        {"A001", 0.86, 0.70, 0.38, 0.62, 0.54, 0.78, 0.72, 0.70},
        {"A004", 0.90, 0.72, 0.34, 0.72, 0.60, 0.74, 0.94, 0.76},
        {"A015", 0.86, 0.66, 0.38, 0.62, 0.52, 0.62, 0.70, 0.74}
    };

    int count = sizeof(assumptions) / sizeof(assumptions[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | risk %.3f | learning %.3f\n",
               assumptions[i].id,
               evidence_adjusted_risk(assumptions[i]),
               learning_value(assumptions[i]));
    }

    return 0;
}
