package main
import "fmt"
type Idea struct{ID string; Stakeholder, Novelty, Evidence, Relevance, Implementation, Source, Safety, Burden float64}
func Score(i Idea) float64{return .14*i.Stakeholder+.14*i.Novelty+.14*i.Evidence+.14*i.Relevance+.10*i.Implementation+.14*i.Source-.10*i.Safety-.10*i.Burden}
func main(){rows:=[]Idea{{"I001",.32,.22,.46,.48,.74,.22,.84,.30},{"I007",.78,.86,.74,.82,.62,.88,.42,.52}}; for _,r:=range rows{fmt.Printf("%s | %.3f
",r.ID,Score(r))}}
