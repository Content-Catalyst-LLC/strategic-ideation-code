#include <iostream>
struct OptionScore{const char* name; double strategic_fit,impact,feasibility,risk_control,learning_value,option_value,ethical_resilience,evidence_confidence;};
double score(const OptionScore& o){return .16*o.strategic_fit+.16*o.impact+.12*o.feasibility+.12*o.risk_control+.14*o.learning_value+.12*o.option_value+.12*o.ethical_resilience+.06*o.evidence_confidence;}
int main(){OptionScore a[]={ {"Core Process Improvement",.78,.66,.82,.72,.38,.34,.58,.78},{"Exploratory Learning Pilot",.62,.58,.66,.54,.86,.78,.64,.52},{"Transformational Platform Bet",.70,.88,.42,.32,.72,.62,.46,.44} }; for(auto&o:a){double s=score(o); std::cout<<o.name<<" | score "<<s<<" | confidence-adjusted "<<s*o.evidence_confidence<<"\n";}}
