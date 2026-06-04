/*
Low-level divergence-convergence process score utilities.
Compile: cc process_score.c -o process_score
Run: ./process_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double exploration;
    double evaluation;
    double iteration;
    double constraints;
    double inclusion;
    double evidence;
    double readiness;
    double memory;
} Context;

double profile_score(Context c) {
    return 0.16 * c.exploration
         + 0.16 * c.evaluation
         + 0.18 * c.iteration
         + 0.14 * c.constraints
         + 0.12 * c.inclusion
         + 0.12 * c.evidence
         + 0.08 * c.readiness
         + 0.04 * c.memory;
}

int main(void) {
    Context contexts[] = {
        {"DC001", 0.28, 0.86, 0.31, 0.71, 0.34, 0.42, 0.79, 0.38},
        {"DC002", 0.74, 0.77, 0.76, 0.73, 0.70, 0.74, 0.81, 0.72},
        {"DC004", 0.79, 0.72, 0.88, 0.69, 0.76, 0.82, 0.77, 0.80}
    };

    int count = sizeof(contexts) / sizeof(contexts[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | %.3f\n", contexts[i].id, profile_score(contexts[i]));
    }

    return 0;
}
