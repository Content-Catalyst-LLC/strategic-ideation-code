# Advanced R workflow for strategic mental-model profiling.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

models <- read.csv(file.path(raw_dir, "mental_model_profiles.csv"))
causal <- read.csv(file.path(raw_dir, "causal_frames.csv"))
evidence <- read.csv(file.path(raw_dir, "evidence_feedback.csv"))

models$adaptive_model_score <-
  0.17 * models$systems_richness +
  0.13 * models$probabilistic_depth +
  0.16 * models$model_flexibility +
  0.14 * models$model_plurality +
  0.16 * models$revision_capacity -
  0.08 * models$institutional_embedding +
  0.12 * models$ethical_visibility +
  0.10 * models$stakeholder_visibility +
  0.10 * models$evidence_responsiveness

models$monoculture_risk <-
  0.28 * models$institutional_embedding +
  0.20 * (1 - models$model_plurality) +
  0.18 * (1 - models$model_flexibility) +
  0.18 * (1 - models$revision_capacity) +
  0.16 * (1 - models$stakeholder_visibility)

models$diagnosis <- ifelse(
  models$adaptive_model_score >= 0.75 & models$monoculture_risk < 0.35,
  "adaptive_model_strength",
  ifelse(
    models$monoculture_risk >= 0.65,
    "model_monoculture_or_lock_in_risk",
    ifelse(
      models$ethical_visibility < 0.45 | models$stakeholder_visibility < 0.45,
      "ethical_or_stakeholder_blind_spot",
      "requires_model_review"
    )
  )
)

causal$causal_adequacy_score <-
  0.24 * causal$environment_fit +
  0.20 * causal$feedback_awareness +
  0.18 * causal$delay_awareness +
  0.18 * causal$nonlinearity_awareness +
  0.20 * causal$second_order_awareness -
  0.18 * causal$blind_spot_risk

evidence$revision_priority <-
  0.40 * evidence$disconfirmation_strength +
  0.30 * evidence$evidence_quality +
  ifelse(evidence$revision_required == "true", 0.20, 0.00) +
  ifelse(evidence$model_response %in% c("treated_as_exception", "delayed_review", "contested"), 0.10, 0.00)

write.csv(models[order(-models$adaptive_model_score), ], file.path(out_tables, "r_mental_model_scores.csv"), row.names = FALSE)
write.csv(causal[order(-causal$causal_adequacy_score), ], file.path(out_tables, "r_causal_frame_scores.csv"), row.names = FALSE)
write.csv(evidence[order(-evidence$revision_priority), ], file.path(out_tables, "r_evidence_revision_priorities.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(models, aes(x = reorder(model_name, adaptive_model_score), y = adaptive_model_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Mental-Model Profile Scores",
      x = "Model",
      y = "Adaptive model score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_mental_model_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_mental_model_scores_base.png"), width = 1100, height = 800)
  barplot(
    models$adaptive_model_score,
    names.arg = models$model_id,
    main = "Strategic Mental-Model Profile Scores",
    ylab = "Adaptive model score"
  )
  dev.off()
}

print(models[, c("model_id", "model_name", "adaptive_model_score", "monoculture_risk", "diagnosis")])
