/*
Low-level strategic creativity score utilities.
Compile: cc creativity_score.c -o creativity_score
Run: ./creativity_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double novelty;
    double relevance;
    double coherence;
    double mechanism;
    double testability;
    double stakeholder;
    double systems;
    double development;
    double risk;
    double revision;
} Idea;

double creativity_score(Idea i) {
    return 0.14 * i.novelty
         + 0.16 * i.relevance
         + 0.13 * i.coherence
         + 0.14 * i.mechanism
         + 0.11 * i.testability
         + 0.13 * i.stakeholder
         + 0.13 * i.systems
         + 0.12 * i.development
         + 0.08 * i.revision
         - 0.12 * i.risk;
}

double novelty_theater_risk(Idea i) {
    return i.novelty * (1.0 - ((i.mechanism + i.stakeholder + i.systems) / 3.0));
}

int main(void) {
    Idea ideas[] = {
        {"I002", 0.72, 0.86, 0.78, 0.80, 0.70, 0.92, 0.78, 0.82, 0.56, 0.82},
        {"I005", 0.76, 0.88, 0.82, 0.84, 0.66, 0.70, 0.90, 0.86, 0.66, 0.86},
        {"I009", 0.70, 0.50, 0.52, 0.34, 0.46, 0.30, 0.32, 0.42, 0.40, 0.38}
    };

    int count = sizeof(ideas) / sizeof(ideas[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | %.3f | novelty risk %.3f\n", ideas[i].id, creativity_score(ideas[i]), novelty_theater_risk(ideas[i]));
    }

    return 0;
}
