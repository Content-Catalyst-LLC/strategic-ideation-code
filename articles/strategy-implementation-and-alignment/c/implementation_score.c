#include <stdio.h>

typedef struct {
    const char *name;
    double goal, coordination, structure, culture, incentives, resources, communication, accountability, adaptation;
} Profile;

double score(Profile p) {
    return 0.12*p.goal + 0.15*p.coordination + 0.12*p.structure + 0.12*p.culture +
           0.13*p.incentives + 0.12*p.resources + 0.11*p.communication + 0.10*p.accountability + 0.10*p.adaptation;
}

int main(void) {
    Profile profiles[] = {
        {"High-Intent Fragmented Organization", 0.70, 0.38, 0.44, 0.31, 0.29, 0.52, 0.41, 0.46, 0.36},
        {"Balanced Aligned Organization", 0.82, 0.81, 0.79, 0.78, 0.77, 0.82, 0.80, 0.76, 0.74},
        {"Adaptive Cross-Functional Organization", 0.78, 0.84, 0.73, 0.76, 0.71, 0.76, 0.78, 0.74, 0.83}
    };
    int count = sizeof(profiles) / sizeof(profiles[0]);
    for (int i = 0; i < count; i++) {
        printf("%s | implementation score %.3f\n", profiles[i].name, score(profiles[i]));
    }
    return 0;
}
