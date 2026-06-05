#include <stdio.h>

typedef struct {
    const char *name;
    double capture, metadata, context, decisions, learning, retrieval, reuse, stewardship, continuity, ethics;
} MemorySystem;

double score(MemorySystem m) {
    return 0.10*m.capture + 0.12*m.metadata + 0.12*m.context + 0.13*m.decisions +
           0.12*m.learning + 0.12*m.retrieval + 0.10*m.reuse +
           0.08*m.stewardship + 0.06*m.continuity + 0.05*m.ethics;
}

int main(void) {
    MemorySystem systems[] = {
        {"Strategic Idea Repository", 0.72, 0.80, 0.76, 0.66, 0.68, 0.78, 0.80, 0.72, 0.70, 0.62},
        {"Decision Memory", 0.70, 0.74, 0.82, 0.86, 0.72, 0.74, 0.76, 0.70, 0.72, 0.70},
        {"Retired Ideas Archive", 0.58, 0.54, 0.56, 0.58, 0.48, 0.52, 0.60, 0.50, 0.48, 0.58}
    };
    int count = sizeof(systems) / sizeof(systems[0]);
    for (int i = 0; i < count; i++) {
        double value = score(systems[i]);
        printf("%s | memory strength %.3f | failure risk %.3f\n", systems[i].name, value, 1.0 - value);
    }
    return 0;
}
