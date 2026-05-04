#include <stdio.h>

int main(void) {
    double values[] = {0.62, 0.86, 0.68, 0.88, 0.74, 0.35, 0.63};
    double weights[] = {0.16, 0.20, 0.16, 0.20, 0.14, -0.08, 0.14};
    int n = 7;
    double score = 0.0;

    for (int i = 0; i < n; i++) {
        score += values[i] * weights[i];
    }

    printf("Synthetic strategic idea score: %.3f\n", score);

    return 0;
}
