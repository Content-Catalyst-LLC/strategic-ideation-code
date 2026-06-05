#include <stdio.h>

typedef struct {
    const char *name;
    double frame, evidence, adaptability, scenario, stakeholder, implementation, ethics, learning, option_value, ai;
} FutureIdea;

double future_ready_score(FutureIdea i) {
    return 0.11*i.frame + 0.11*i.evidence + 0.11*i.adaptability + 0.12*i.scenario +
           0.11*i.stakeholder + 0.10*i.implementation + 0.11*i.ethics + 0.12*i.learning +
           0.07*i.option_value + 0.04*i.ai;
}

int main(void) {
    FutureIdea ideas[] = {
        {"Scenario-Linked Option Portfolio", 0.78, 0.72, 0.84, 0.86, 0.70, 0.70, 0.76, 0.86, 0.90, 0.62},
        {"Participatory Strategy Lab", 0.80, 0.74, 0.78, 0.72, 0.86, 0.64, 0.84, 0.78, 0.72, 0.56},
        {"Rapid Automation Initiative", 0.54, 0.52, 0.48, 0.46, 0.42, 0.50, 0.44, 0.42, 0.46, 0.38}
    };

    int count = sizeof(ideas) / sizeof(ideas[0]);
    for (int i = 0; i < count; i++) {
        double score = future_ready_score(ideas[i]);
        printf("%s | future-ready score %.3f | future risk %.3f\n", ideas[i].name, score, 1.0 - score);
    }
    return 0;
}
