/*
Low-level lateral thinking score utilities.
Compile: cc lateral_score.c -o lateral_score
Run: ./lateral_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double rigidity;
    double provocation;
    double analogy;
    double random_entry;
    double reversal;
    double challenge;
    double convergence;
    double systems;
    double legitimacy;
    double political_safety;
    double transformation;
} Context;

double lateral_profile(Context c) {
    return -0.14 * c.rigidity
         + 0.14 * c.provocation
         + 0.12 * c.analogy
         + 0.09 * c.random_entry
         + 0.10 * c.reversal
         + 0.10 * c.challenge
         + 0.14 * c.convergence
         + 0.12 * c.systems
         + 0.08 * c.legitimacy
         + 0.07 * c.political_safety
         + 0.14 * c.transformation;
}

int main(void) {
    Context contexts[] = {
        {"LT001", 0.86, 0.18, 0.21, 0.16, 0.20, 0.28, 0.72, 0.44, 0.50, 0.48, 0.24},
        {"LT004", 0.36, 0.74, 0.76, 0.70, 0.78, 0.80, 0.82, 0.86, 0.78, 0.74, 0.88},
        {"LT008", 0.52, 0.78, 0.68, 0.72, 0.70, 0.46, 0.28, 0.34, 0.36, 0.40, 0.62}
    };

    int count = sizeof(contexts) / sizeof(contexts[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | %.3f\n", contexts[i].id, lateral_profile(contexts[i]));
    }

    return 0;
}
