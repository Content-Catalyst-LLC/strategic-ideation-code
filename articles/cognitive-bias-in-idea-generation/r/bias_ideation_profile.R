root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw"); out_tables <- file.path(root, "outputs", "tables"); out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE); dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)
contexts <- read.csv(file.path(raw_dir, "bias_contexts.csv"))
contexts$bias_adjusted_ideation_profile <- -0.12*contexts$availability_pressure -0.12*contexts$anchoring_intensity -0.13*contexts$conformity_pressure -0.12*contexts$framing_rigidity -0.10*contexts$institutional_lock_in -0.08*contexts$expert_enclosure -0.07*contexts$ai_familiarity_pressure +0.16*contexts$stakeholder_diversity +0.18*contexts$exploratory_variation +0.12*contexts$evidence_discipline +0.08*contexts$political_safety +0.08*contexts$decision_memory_quality
contexts$premature_convergence_risk <- contexts$anchoring_intensity * contexts$conformity_pressure * contexts$framing_rigidity
write.csv(contexts[order(-contexts$bias_adjusted_ideation_profile), ], file.path(out_tables, "r_bias_context_profiles.csv"), row.names = FALSE)
png(file.path(out_figures, "r_bias_context_profiles_base.png"), width = 1100, height = 800); barplot(contexts$bias_adjusted_ideation_profile, names.arg = contexts$context_id, main = "Bias-Adjusted Ideation Profile Scores", ylab = "Profile score"); dev.off()
print(contexts[, c("context_id", "context_name", "bias_adjusted_ideation_profile", "premature_convergence_risk")])
