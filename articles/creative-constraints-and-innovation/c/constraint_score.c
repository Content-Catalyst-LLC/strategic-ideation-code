/*
Low-level creative constraint score utilities.
Compile: cc constraint_score.c -o constraint_score
Run: ./constraint_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double resource;
    double technical;
    double institutional;
    double ecological;
    double ethics;
    double focus;
    double opportunity;
    double legitimacy;
    double learning;
    double readiness;
} Context;

double productive_profile(Context c) {
    return -0.10 * c.resource
         - 0.10 * c.technical
         - 0.10 * c.institutional
         + 0.12 * c.ecological
         + 0.16 * c.ethics
         + 0.16 * c.focus
         + 0.16 * c.opportunity
         + 0.14 * c.legitimacy
         + 0.14 * c.learning
         + 0.12 * c.readiness;
}

int main(void) {
    Context contexts[] = {
        {"CC001", 0.12, 0.18, 0.16, 0.20, 0.38, 0.24, 0.38, 0.42, 0.36, 0.34},
        {"CC002", 0.54, 0.47, 0.43, 0.52, 0.66, 0.78, 0.81, 0.72, 0.78, 0.76},
        {"CC007", 0.66, 0.52, 0.57, 0.92, 0.88, 0.74, 0.70, 0.82, 0.76, 0.60}
    };

    int count = sizeof(contexts) / sizeof(contexts[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | %.3f\n", contexts[i].id, productive_profile(contexts[i]));
    }

    return 0;
}
