#include <iostream>
struct Option { const char* id; double fit, constraints, mechanisms, evidence, ethics, feasibility, uncertainty; };
double score(Option o){ return .18*o.fit + .16*o.constraints + .20*o.mechanisms + .14*o.evidence + .16*o.ethics + .14*o.feasibility - .08*o.uncertainty; }
int main(){ Option options[]={{"O004",.91,.88,.90,.80,.86,.66,.31},{"O008",.90,.79,.91,.74,.85,.65,.34}}; for(auto o: options){ std::cout << o.id << " | " << score(o) << "\n"; } }
