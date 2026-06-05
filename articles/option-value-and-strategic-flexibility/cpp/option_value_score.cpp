#include <iostream>
#include <string>
#include <vector>
struct O { std::string name; double initial, learning, flex, rev, scale, mod, lockin, cost, gov, ethics; };
double score(const O& o){ return .10*o.initial+.17*o.learning+.17*o.flex+.12*o.rev+.11*o.scale+.13*o.mod-.14*o.lockin-.06*o.cost+.11*o.gov+.09*o.ethics; }
double warning(const O& o){ return .30*o.lockin+.18*(1-o.rev)+.16*(1-o.flex)+.14*(1-o.mod)+.12*(1-o.gov)+.10*(1-o.ethics); }
int main(){ std::vector<O> v={{"Pilot Before Scale",.58,.82,.78,.74,.70,.64,.32,.46,.70,.68},{"Full Commitment Now",.86,.30,.28,.22,.80,.24,.82,.34,.48,.36}}; for(const auto& o:v) std::cout<<o.name<<" | option value "<<score(o)<<" | lock-in warning "<<warning(o)<<"
"; }
