package main
import "fmt"
type OptionScore struct{Name string; StrategicFit,Impact,Feasibility,RiskControl,LearningValue,OptionValue,EthicalResilience,EvidenceConfidence float64}
func Score(o OptionScore) float64{return .16*o.StrategicFit+.16*o.Impact+.12*o.Feasibility+.12*o.RiskControl+.14*o.LearningValue+.12*o.OptionValue+.12*o.EthicalResilience+.06*o.EvidenceConfidence}
func main(){options:=[]OptionScore{{"Core Process Improvement",.78,.66,.82,.72,.38,.34,.58,.78},{"Exploratory Learning Pilot",.62,.58,.66,.54,.86,.78,.64,.52},{"Transformational Platform Bet",.70,.88,.42,.32,.72,.62,.46,.44}}; for _,o:=range options{s:=Score(o); fmt.Printf("%s | score %.3f | confidence-adjusted %.3f\n",o.Name,s,s*o.EvidenceConfidence)}}
