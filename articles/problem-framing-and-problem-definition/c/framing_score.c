/*
Low-level problem-framing score utilities.
Compile: cc framing_score.c -o framing_score
Run: ./framing_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double boundary;
    double stakeholder;
    double systems;
    double causal;
    double assumptions;
    double reframing;
    double actionability;
    double lock_in;
    double politics;
} Frame;

double framing_score(Frame f) {
    return 0.16 * f.boundary
         + 0.15 * f.stakeholder
         + 0.15 * f.systems
         + 0.16 * f.causal
         + 0.12 * f.assumptions
         + 0.13 * f.reframing
         + 0.11 * f.actionability
         - 0.10 * f.lock_in
         - 0.08 * f.politics;
}

double symptom_risk(Frame f) {
    double boundary_gap = 0.70 - f.boundary;
    if (boundary_gap < 0.0) boundary_gap = 0.0;

    return (1.0 - f.causal) * 0.30
         + (1.0 - f.systems) * 0.25
         + boundary_gap * 0.20
         + f.lock_in * 0.15
         + f.politics * 0.10;
}

int main(void) {
    Frame frames[] = {
        {"F001", 0.28, 0.34, 0.26, 0.31, 0.24, 0.22, 0.62, 0.82, 0.70},
        {"F003", 0.86, 0.79, 0.91, 0.84, 0.78, 0.82, 0.72, 0.32, 0.34},
        {"F005", 0.82, 0.92, 0.78, 0.74, 0.76, 0.80, 0.74, 0.34, 0.30}
    };

    int count = sizeof(frames) / sizeof(frames[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | score %.3f | symptom risk %.3f\n",
               frames[i].id,
               framing_score(frames[i]),
               symptom_risk(frames[i]));
    }

    return 0;
}
