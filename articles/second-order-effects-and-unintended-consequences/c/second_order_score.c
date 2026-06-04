/*
Low-level second-order effects score utilities.
Compile: cc second_order_score.c -o second_order_score
Run: ./second_order_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double first_gain;
    double adaptation;
    double feedback;
    double delay;
    double burden;
    double gaming;
    double fragility;
    double learning;
    double legitimacy;
    double reversibility;
} Intervention;

double second_order_risk(Intervention i) {
    return 0.16 * i.adaptation
         + 0.15 * i.feedback
         + 0.14 * i.delay
         + 0.15 * i.burden
         + 0.14 * i.gaming
         + 0.16 * i.fragility
         - 0.10 * i.learning
         - 0.06 * i.legitimacy
         - 0.06 * i.reversibility;
}

double false_success_risk(Intervention i) {
    return 0.26 * i.first_gain
         + 0.20 * i.fragility
         + 0.16 * i.delay
         + 0.14 * i.gaming
         + 0.12 * i.burden
         - 0.16 * i.learning;
}

int main(void) {
    Intervention interventions[] = {
        {"I001", 0.88, 0.76, 0.58, 0.69, 0.66, 0.52, 0.82, 0.38, 0.44, 0.42},
        {"I002", 0.71, 0.44, 0.51, 0.42, 0.34, 0.28, 0.39, 0.76, 0.72, 0.70},
        {"I003", 0.63, 0.81, 0.73, 0.57, 0.78, 0.74, 0.74, 0.42, 0.46, 0.38}
    };

    int count = sizeof(interventions) / sizeof(interventions[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | second-order risk %.3f | false-success risk %.3f\n",
               interventions[i].id,
               second_order_risk(interventions[i]),
               false_success_risk(interventions[i]));
    }

    return 0;
}
