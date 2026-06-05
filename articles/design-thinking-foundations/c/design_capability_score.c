/*
Low-level design capability utilities.
Compile: cc design_capability_score.c -o design_capability_score
Run: ./design_capability_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double empathy;
    double reframing;
    double divergence;
    double convergence;
    double prototyping;
    double testing;
    double systems;
    double ethics;
    double decision;
    double adaptability;
    double memory;
} DesignContext;

double capability(DesignContext c) {
    return 0.12 * c.empathy +
           0.13 * c.reframing +
           0.10 * c.divergence +
           0.10 * c.convergence +
           0.12 * c.prototyping +
           0.12 * c.testing +
           0.11 * c.systems +
           0.10 * c.ethics +
           0.10 * c.decision +
           0.06 * c.adaptability +
           0.04 * c.memory;
}

double superficiality_risk(DesignContext c) {
    return 0.18 * (1.0 - c.empathy) +
           0.14 * (1.0 - c.reframing) +
           0.12 * (1.0 - c.testing) +
           0.12 * (1.0 - c.systems) +
           0.12 * (1.0 - c.ethics) +
           0.16 * (1.0 - c.decision) +
           0.10 * (1.0 - c.memory) +
           0.06 * (1.0 - c.adaptability);
}

int main(void) {
    DesignContext contexts[] = {
        {"C001", 0.28, 0.31, 0.36, 0.58, 0.24, 0.29, 0.35, 0.42, 0.36, 0.33, 0.40},
        {"C003", 0.81, 0.84, 0.86, 0.74, 0.88, 0.86, 0.72, 0.74, 0.78, 0.89, 0.76},
        {"C004", 0.39, 0.34, 0.68, 0.38, 0.41, 0.36, 0.30, 0.34, 0.28, 0.42, 0.24}
    };

    int count = sizeof(contexts) / sizeof(contexts[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | capability %.3f | superficiality risk %.3f\n",
               contexts[i].id,
               capability(contexts[i]),
               superficiality_risk(contexts[i]));
    }

    return 0;
}
