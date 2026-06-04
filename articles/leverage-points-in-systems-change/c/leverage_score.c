/*
Low-level leverage-point score utilities.
Compile: cc leverage_score.c -o leverage_score
Run: ./leverage_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double implementation_ease;
    double structural_depth;
    double system_sensitivity;
    double feedback_influence;
    double information_effect;
    double rule_power;
    double goal_alignment;
    double paradigm_relevance;
    double transformative_potential;
    double legitimacy_requirement;
    double unintended_risk;
    double learning_capacity;
} LeveragePoint;

double leverage_score(LeveragePoint l) {
    return 0.06 * l.implementation_ease
         + 0.16 * l.structural_depth
         + 0.14 * l.system_sensitivity
         + 0.13 * l.feedback_influence
         + 0.11 * l.information_effect
         + 0.13 * l.rule_power
         + 0.13 * l.goal_alignment
         + 0.08 * l.paradigm_relevance
         + 0.14 * l.transformative_potential
         + 0.08 * l.learning_capacity
         - 0.06 * l.unintended_risk;
}

double governance_need(LeveragePoint l) {
    return 0.26 * l.legitimacy_requirement
         + 0.24 * l.unintended_risk
         + 0.22 * l.transformative_potential
         + 0.14 * (1.0 - l.implementation_ease)
         + 0.14 * l.paradigm_relevance;
}

int main(void) {
    LeveragePoint points[] = {
        {"L001", 0.86, 0.22, 0.28, 0.28, 0.31, 0.20, 0.28, 0.16, 0.24, 0.24, 0.26, 0.34},
        {"L006", 0.44, 0.82, 0.82, 0.76, 0.66, 0.90, 0.78, 0.58, 0.82, 0.72, 0.70, 0.70},
        {"L008", 0.21, 0.96, 0.88, 0.82, 0.60, 0.78, 0.96, 0.98, 0.96, 0.90, 0.82, 0.78}
    };

    int count = sizeof(points) / sizeof(points[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | leverage %.3f | governance need %.3f\n",
               points[i].id,
               leverage_score(points[i]),
               governance_need(points[i]));
    }

    return 0;
}
