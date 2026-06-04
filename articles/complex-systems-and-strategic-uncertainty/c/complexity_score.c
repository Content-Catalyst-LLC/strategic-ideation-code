/*
Low-level complexity profile score utilities.
Compile: cc complexity_score.c -o complexity_score
Run: ./complexity_score
*/

#include <stdio.h>

typedef struct {
    const char *id;
    double interdependence;
    double nonlinearity;
    double feedback;
    double adaptation;
    double path;
    double boundary;
    double emergence;
    double deep_uncertainty;
    double scenario_need;
    double learning_need;
} Environment;

double complexity_score(Environment e) {
    return 0.13 * e.interdependence
         + 0.13 * e.nonlinearity
         + 0.14 * e.feedback
         + 0.12 * e.adaptation
         + 0.11 * e.path
         + 0.10 * e.boundary
         + 0.10 * e.emergence
         + 0.09 * e.deep_uncertainty
         + 0.09 * e.scenario_need
         + 0.09 * e.learning_need;
}

double linear_planning_risk(Environment e) {
    return 0.20 * e.nonlinearity
         + 0.20 * e.feedback
         + 0.18 * e.adaptation
         + 0.16 * e.deep_uncertainty
         + 0.14 * e.boundary
         + 0.12 * e.emergence;
}

int main(void) {
    Environment environments[] = {
        {"ENV001", 0.32, 0.24, 0.31, 0.28, 0.36, 0.30, 0.26, 0.28, 0.30, 0.34},
        {"ENV003", 0.81, 0.74, 0.79, 0.71, 0.78, 0.76, 0.74, 0.82, 0.82, 0.80},
        {"ENV004", 0.88, 0.86, 0.87, 0.82, 0.84, 0.82, 0.86, 0.90, 0.90, 0.88}
    };

    int count = sizeof(environments) / sizeof(environments[0]);

    for (int i = 0; i < count; i++) {
        printf("%s | complexity %.3f | linear planning risk %.3f\n",
               environments[i].id,
               complexity_score(environments[i]),
               linear_planning_risk(environments[i]));
    }

    return 0;
}
