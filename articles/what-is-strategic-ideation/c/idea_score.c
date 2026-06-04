/*
Low-level idea-score utilities.
Compile: cc idea_score.c -o idea_score
Run: ./idea_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double strategic_fit;
    double feasibility;
    double systems_leverage;
    double learning_value;
    double uncertainty;
} Idea;

double idea_score(Idea idea) {
    return 0.28 * idea.strategic_fit
         + 0.18 * idea.feasibility
         + 0.24 * idea.systems_leverage
         + 0.18 * idea.learning_value
         - 0.12 * idea.uncertainty;
}

int main(void) {
    Idea ideas[] = {
        {"I001", 0.91, 0.82, 0.74, 0.88, 0.24},
        {"I004", 0.78, 0.76, 0.65, 0.95, 0.28},
        {"I008", 0.86, 0.70, 0.89, 0.88, 0.37}
    };

    int count = sizeof(ideas) / sizeof(ideas[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | %.3f\n", ideas[i].id, idea_score(ideas[i]));
    }

    return 0;
}
