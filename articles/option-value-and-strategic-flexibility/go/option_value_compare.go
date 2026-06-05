package main
import "fmt"
type OptionProfile struct { Name string; InitialReturn, Learning, Flexibility, Reversibility, Scalability, Modularity, LockIn, CarryingCost, Governance, Ethics float64 }
func Score(o OptionProfile) float64 { return 0.10*o.InitialReturn + 0.17*o.Learning + 0.17*o.Flexibility + 0.12*o.Reversibility + 0.11*o.Scalability + 0.13*o.Modularity - 0.14*o.LockIn - 0.06*o.CarryingCost + 0.11*o.Governance + 0.09*o.Ethics }
func Warning(o OptionProfile) float64 { return 0.30*o.LockIn + 0.18*(1-o.Reversibility) + 0.16*(1-o.Flexibility) + 0.14*(1-o.Modularity) + 0.12*(1-o.Governance) + 0.10*(1-o.Ethics) }
func main() { options := []OptionProfile{{"Pilot Before Scale",0.58,0.82,0.78,0.74,0.70,0.64,0.32,0.46,0.70,0.68},{"Full Commitment Now",0.86,0.30,0.28,0.22,0.80,0.24,0.82,0.34,0.48,0.36}}; for _, o := range options { fmt.Printf("%s | option value %.3f | lock-in warning %.3f
", o.Name, Score(o), Warning(o)) } }
