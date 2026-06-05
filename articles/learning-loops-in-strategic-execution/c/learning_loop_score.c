#include <stdio.h>

typedef struct {
    const char *name;
    double feedback, assumptions, interpretation, authority, closure, memory, safety, scaling, ethics;
} Context;

double score(Context c) {
    return 0.13*c.feedback + 0.13*c.assumptions + 0.12*c.interpretation +
           0.14*c.authority + 0.14*c.closure + 0.10*c.memory +
           0.09*c.safety + 0.08*c.scaling + 0.07*c.ethics;
}

int main(void) {
    Context contexts[] = {
        {"Reporting-Heavy Organization", 0.62, 0.42, 0.46, 0.38, 0.34, 0.36, 0.44, 0.40, 0.50},
        {"Adaptive Learning Organization", 0.84, 0.82, 0.80, 0.78, 0.82, 0.76, 0.78, 0.74, 0.80},
        {"Pilot-Rich Memory-Poor Organization", 0.72, 0.60, 0.62, 0.56, 0.48, 0.30, 0.58, 0.36, 0.56}
    };
    int count = sizeof(contexts) / sizeof(contexts[0]);
    for (int i = 0; i < count; i++) {
        double value = score(contexts[i]);
        printf("%s | learning loop strength %.3f | learning debt %.3f\n",
               contexts[i].name, value, 1.0 - value);
    }
    return 0;
}
