/*
Low-level alignment-score utility.
Compile: cc alignment_score.c -o alignment_score
Run: ./alignment_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double ideation;
    double strategy;
    double tactics;
    double feedback;
    double learning;
} LayerContext;

double alignment_score(LayerContext c) {
    return 0.18 * c.ideation
         + 0.24 * c.strategy
         + 0.22 * c.tactics
         + 0.18 * c.feedback
         + 0.18 * c.learning;
}

const char *diagnosis(LayerContext c) {
    if (c.tactics >= 0.65 && c.strategy < 0.55) return "tactical_overload";
    if (c.ideation >= 0.75 && c.strategy < 0.55) return "selection_gap";
    if (c.strategy >= 0.70 && c.tactics < 0.55) return "translation_gap";
    if (c.feedback < 0.55 || c.learning < 0.55) return "learning_gap";
    return "monitor";
}

int main(void) {
    LayerContext contexts[] = {
        {"C001", 0.32, 0.28, 0.39, 0.31, 0.27},
        {"C002", 0.74, 0.79, 0.77, 0.75, 0.76},
        {"C003", 0.89, 0.41, 0.34, 0.42, 0.46}
    };

    int count = sizeof(contexts) / sizeof(contexts[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | %.3f | %s\n", contexts[i].id, alignment_score(contexts[i]), diagnosis(contexts[i]));
    }

    return 0;
}
