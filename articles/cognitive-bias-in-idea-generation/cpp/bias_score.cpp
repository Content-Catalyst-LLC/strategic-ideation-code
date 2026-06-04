#include <iostream>
struct C{const char* id; double a,n,c,f,i,e,ai,s,v,ev,p,m;};
double score(C x){return -.12*x.a-.12*x.n-.13*x.c-.12*x.f-.10*x.i-.08*x.e-.07*x.ai+.16*x.s+.18*x.v+.12*x.ev+.08*x.p+.08*x.m;}
int main(){C rows[]={{"CB001",.84,.71,.63,.77,.66,.58,.62,.34,.28,.48,.46,.34},{"CB004",.32,.29,.27,.31,.30,.34,.36,.82,.89,.76,.74,.72}};for(auto r:rows)std::cout<<r.id<<" | "<<score(r)<<"
";}
