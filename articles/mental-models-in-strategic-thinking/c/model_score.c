/*
Low-level mental-model score utilities.
Compile: cc model_score.c -o model_score
Run: ./model_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double systems;
    double probability;
    double flexibility;
    double plurality;
    double revision;
    double embedding;
    double ethics;
    double stakeholder;
    double evidence;
} Model;

double adaptive_score(Model m) {
    return 0.17 * m.systems
         + 0.13 * m.probability
         + 0.16 * m.flexibility
         + 0.14 * m.plurality
         + 0.16 * m.revision
         - 0.08 * m.embedding
         + 0.12 * m.ethics
         + 0.10 * m.stakeholder
         + 0.10 * m.evidence;
}

int main(void) {
    Model models[] = {
        {"M001", 0.24, 0.21, 0.19, 0.22, 0.22, 0.58, 0.31, 0.28, 0.34},
        {"M003", 0.89, 0.84, 0.88, 0.86, 0.87, 0.71, 0.82, 0.80, 0.86},
        {"M010", 0.82, 0.67, 0.78, 0.84, 0.79, 0.52, 0.93, 0.94, 0.78}
    };

    int count = sizeof(models) / sizeof(models[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | %.3f\n", models[i].id, adaptive_score(models[i]));
    }

    return 0;
}
