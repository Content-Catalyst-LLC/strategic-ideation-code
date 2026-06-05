/*
Low-level opportunity score utilities.
Compile: cc opportunity_score.c -o opportunity_score
Run: ./opportunity_score
*/

#include <stdio.h>

typedef struct {
    const char *name;
    double signal;
    double capability;
    double desirability;
    double viability;
    double timing;
    double learning;
    double option_value;
    double strategic_fit;
    double ethics;
    double risk;
    double confidence;
} OpportunityProfile;

double profile_score(OpportunityProfile o) {
    return 0.13 * o.signal +
           0.14 * o.capability +
           0.12 * o.desirability +
           0.12 * o.viability +
           0.10 * o.timing +
           0.12 * o.learning +
           0.11 * o.option_value +
           0.10 * o.strategic_fit +
           0.10 * o.ethics -
           0.14 * o.risk;
}

int main(void) {
    OpportunityProfile opportunities[] = {
        {"Emerging Technology Adjacency", 0.74, 0.78, 0.72, 0.71, 0.76, 0.70, 0.66, 0.78, 0.62, 0.46, 0.68},
        {"High-Hype Weak-Fit Opportunity", 0.86, 0.31, 0.77, 0.39, 0.48, 0.62, 0.44, 0.40, 0.42, 0.78, 0.38},
        {"Slow-Build Sustainability Opportunity", 0.62, 0.73, 0.81, 0.74, 0.67, 0.64, 0.72, 0.76, 0.82, 0.41, 0.66}
    };

    int count = sizeof(opportunities) / sizeof(opportunities[0]);

    for (int i = 0; i < count; i++) {
        double score = profile_score(opportunities[i]);
        printf("%s | score %.3f | confidence-adjusted %.3f\n",
               opportunities[i].name,
               score,
               score * opportunities[i].confidence);
    }

    return 0;
}
