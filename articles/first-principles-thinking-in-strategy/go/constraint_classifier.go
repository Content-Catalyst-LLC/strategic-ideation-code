package main
import "fmt"
type Constraint struct { ID string; IsReal bool; Certainty, Importance, Redesign, Evidence float64 }
func Priority(c Constraint) float64 { if c.IsReal { return c.Importance*c.Certainty*(1-c.Redesign) }; return c.Importance*c.Redesign*(1-c.Evidence+0.25) }
func main() { for _, c := range []Constraint{{"C001",false,.62,.82,.78,.54},{"C005",true,.86,.93,.08,.82}} { fmt.Printf("%s | %.3f\n", c.ID, Priority(c)) } }
