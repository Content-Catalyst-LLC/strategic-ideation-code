using DelimitedFiles
root=normpath(joinpath(@__DIR__,"..")); raw=joinpath(root,"data","raw"); out=joinpath(root,"outputs","tables"); mkpath(out)
scores=readdlm(joinpath(raw,"scores.csv"), ',', String); weights=readdlm(joinpath(raw,"weight_sets.csv"), ',', String)
sh=scores[1,:]; wh=weights[1,:]; sr=scores[2:end,:]; wr=weights[2:end,:]
criteria=["strategic_fit","impact","feasibility","risk_control","learning_value","option_value","ethical_resilience","evidence_confidence"]
scol(n)=findfirst(==(n),sh); wcol(n)=findfirst(==(n),wh); snum(r,n)=parse(Float64,r[scol(n)]); wnum(r,n)=parse(Float64,r[wcol(n)])
output=[["weight_set","option_id","weighted_score","confidence_adjusted_score"]]
for i in 1:size(wr,1)
  for j in 1:size(sr,1)
    score=sum(wnum(wr[i,:],c)*snum(sr[j,:],c) for c in criteria)
    push!(output,[wr[i,wcol("weight_set")],sr[j,scol("option_id")],round(score,digits=4),round(score*snum(sr[j,:],"evidence_confidence"),digits=4)])
  end
end
writedlm(joinpath(out,"julia_matrix_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_matrix_sensitivity.csv")
