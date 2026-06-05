/*
Low-level game-theory score utilities.
Compile: cc game_theory_score.c -o game_theory_score
Run: ./game_theory_score
*/

#include <stdio.h>

typedef struct {
    const char *name;
    double rivalry;
    double coordination;
    double information_asymmetry;
    double retaliation;
    double institutional_support;
    double behavioral_realism;
    double mechanism_design;
    double ethical_complexity;
} Setting;

double mechanism_opportunity(Setting s) {
    return 0.30 * s.mechanism_design +
           0.18 * s.coordination +
           0.16 * s.information_asymmetry +
           0.14 * s.ethical_complexity +
           0.12 * s.institutional_support +
           0.10 * s.behavioral_realism;
}

double cooperation_fragility(Setting s) {
    return 0.22 * s.rivalry +
           0.20 * s.retaliation +
           0.16 * s.information_asymmetry +
           0.12 * s.ethical_complexity -
           0.15 * s.institutional_support -
           0.15 * s.coordination;
}

int main(void) {
    Setting settings[] = {
        {"Price Competition Environment", 0.84, 0.28, 0.44, 0.76, 0.39, 0.52, 0.42, 0.46},
        {"Standards Coordination Environment", 0.36, 0.86, 0.31, 0.24, 0.73, 0.68, 0.78, 0.54},
        {"Platform Ecosystem Environment", 0.71, 0.74, 0.69, 0.58, 0.57, 0.74, 0.82, 0.76}
    };

    int count = sizeof(settings) / sizeof(settings[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | mechanism opportunity %.3f | cooperation fragility %.3f\n",
               settings[i].name,
               mechanism_opportunity(settings[i]),
               cooperation_fragility(settings[i]));
    }

    return 0;
}
