#include <stdio.h>

typedef struct {
    const char *name;
    double structure, clarity, evidence, assumptions, narrative, decision, modularity, reuse, governance, ethics;
} Framework;

double score(Framework f) {
    return 0.11*f.structure + 0.11*f.clarity + 0.12*f.evidence + 0.10*f.assumptions +
           0.10*f.narrative + 0.13*f.decision + 0.10*f.modularity +
           0.10*f.reuse + 0.08*f.governance + 0.05*f.ethics;
}

int main(void) {
    Framework frameworks[] = {
        {"Idea Record Framework", 0.76, 0.72, 0.66, 0.68, 0.62, 0.64, 0.74, 0.72, 0.66, 0.60},
        {"Decision Memo Framework", 0.82, 0.76, 0.80, 0.78, 0.74, 0.86, 0.66, 0.68, 0.72, 0.72},
        {"AI-Assisted Ideation Framework", 0.62, 0.56, 0.50, 0.48, 0.58, 0.54, 0.60, 0.58, 0.46, 0.42}
    };
    int count = sizeof(frameworks) / sizeof(frameworks[0]);
    for (int i = 0; i < count; i++) {
        double value = score(frameworks[i]);
        printf("%s | framework strength %.3f | risk %.3f\n", frameworks[i].name, value, 1.0 - value);
    }
    return 0;
}
