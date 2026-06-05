args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) script_path <- "r/matrix_sensitivity_review.R"
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw <- file.path(root, "data", "raw"); out <- file.path(root, "outputs", "tables"); fig <- file.path(root, "outputs", "figures")
dir.create(out, recursive=TRUE, showWarnings=FALSE); dir.create(fig, recursive=TRUE, showWarnings=FALSE)
options <- read.csv(file.path(raw,"options.csv")); scores <- read.csv(file.path(raw,"scores.csv")); weights <- read.csv(file.path(raw,"weight_sets.csv"))
criteria <- c("strategic_fit","impact","feasibility","risk_control","learning_value","option_value","ethical_resilience","evidence_confidence")
results <- data.frame()
for (i in seq_len(nrow(weights))) {
  w <- as.numeric(weights[i, criteria]); sc <- as.vector(as.matrix(scores[,criteria]) %*% w)
  temp <- data.frame(weight_set=weights$weight_set[i], option_id=scores$option_id, score=sc)
  temp <- merge(temp, options[,c("option_id","option_name")], by="option_id")
  temp$rank <- rank(-temp$score, ties.method="min")
  results <- rbind(results,temp)
}
write.csv(results,file.path(out,"r_matrix_weight_sensitivity.csv"),row.names=FALSE)
if (requireNamespace("ggplot2", quietly=TRUE)) {
  library(ggplot2)
  ggplot(results,aes(x=reorder(option_name,score),y=score,fill=weight_set))+geom_col(position="dodge")+coord_flip()+theme_minimal(base_size=12)+labs(title="Decision Matrix Scores Across Weight Sets",x="Option",y="Score")
  ggsave(file.path(fig,"r_matrix_weight_sensitivity.png"), width=11, height=8, dpi=160)
}
print(results)
