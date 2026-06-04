#include <stdio.h>
typedef struct { const char *id; double assumptions, clarity, constraints, reconstruction, adaptation; } Context;
double score(Context c){ return -.16*c.assumptions + .18*c.clarity + .18*c.constraints + .18*c.reconstruction + .14*c.adaptation; }
int main(void){ Context contexts[]={{"FP001",.84,.31,.28,.34,.39},{"FP003",.22,.88,.91,.89,.92}}; for(int i=0;i<2;i++) printf("%s | %.3f\n", contexts[i].id, score(contexts[i])); return 0; }
