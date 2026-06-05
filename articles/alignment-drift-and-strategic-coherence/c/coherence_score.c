#include <stdio.h>

typedef struct {
    const char *name;
    double purpose, priority, tradeoff, resources, incentives, interpretation, governance, feedback, memory, ethics;
} Context;

double score(Context c) {
    return 0.15*c.purpose + 0.12*c.priority + 0.11*c.tradeoff + 0.13*c.resources +
           0.13*c.incentives + 0.11*c.interpretation + 0.12*c.governance +
           0.08*c.feedback + 0.07*c.memory + 0.08*c.ethics;
}

int main(void) {
    Context contexts[] = {
        {"Symbolically Aligned Organization", 0.64, 0.50, 0.46, 0.46, 0.42, 0.50, 0.44, 0.48, 0.40, 0.54},
        {"Coherent Adaptive Organization", 0.84, 0.80, 0.78, 0.78, 0.80, 0.82, 0.78, 0.84, 0.76, 0.80},
        {"Metric-Substituted Organization", 0.68, 0.60, 0.54, 0.62, 0.36, 0.58, 0.52, 0.44, 0.50, 0.46}
    };
    int count = sizeof(contexts) / sizeof(contexts[0]);
    for (int i = 0; i < count; i++) {
        double value = score(contexts[i]);
        printf("%s | coherence %.3f | drift risk %.3f\n", contexts[i].name, value, 1.0 - value);
    }
    return 0;
}
