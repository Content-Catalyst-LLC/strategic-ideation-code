#include <stdio.h>

typedef struct {
    const char *name;
    double category, level, maturity, evidence, function, relationships, retrieval, governance, ethics;
} TaxonomyRecord;

double score(TaxonomyRecord t) {
    return 0.13*t.category + 0.11*t.level + 0.11*t.maturity + 0.12*t.evidence +
           0.13*t.function + 0.11*t.relationships + 0.13*t.retrieval +
           0.09*t.governance + 0.07*t.ethics;
}

int main(void) {
    TaxonomyRecord records[] = {
        {"Strategic Learning Repository", 0.78, 0.76, 0.72, 0.72, 0.80, 0.76, 0.82, 0.74, 0.66},
        {"Participatory Governance Prototype", 0.76, 0.74, 0.76, 0.70, 0.74, 0.72, 0.76, 0.70, 0.82},
        {"Advisory Panel Without Authority", 0.66, 0.62, 0.72, 0.62, 0.60, 0.66, 0.62, 0.56, 0.76}
    };
    int count = sizeof(records) / sizeof(records[0]);
    for (int i = 0; i < count; i++) {
        double value = score(records[i]);
        printf("%s | taxonomy strength %.3f | taxonomy risk %.3f\n", records[i].name, value, 1.0 - value);
    }
    return 0;
}
