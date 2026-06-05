# Advanced R workflow for alignment drift and coherence profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/alignment_drift_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "coherence_contexts.csv"))

contexts$strategic_coherence_score <-
  0.13 * contexts$purpose_clarity +
  0.12 * contexts$priority_discipline +
  0.11 * contexts$tradeoff_integrity +
  0.12 * contexts$resource_alignment +
  0.12 * contexts$incentive_fit +
  0.10 * contexts$interpretive_consistency +
  0.11 * contexts$governance_strength +
  0.09 * contexts$feedback_quality +
  0.06 * contexts$decision_memory +
  0.07 * contexts$ethical_coherence +
  0.07 * contexts$adaptive_capacity

contexts$alignment_drift_risk <-
  0.13 * (1 - contexts$purpose_clarity) +
  0.12 * (1 - contexts$priority_discipline) +
  0.11 * (1 - contexts$tradeoff_integrity) +
  0.12 * (1 - contexts$resource_alignment) +
  0.13 * (1 - contexts$incentive_fit) +
  0.10 * (1 - contexts$interpretive_consistency) +
  0.11 * (1 - contexts$governance_strength) +
  0.08 * (1 - contexts$feedback_quality) +
  0.06 * (1 - contexts$decision_memory) +
  0.07 * (1 - contexts$ethical_coherence) +
  0.07 * (1 - contexts$adaptive_capacity)

write.csv(
  contexts[order(-contexts$strategic_coherence_score), ],
  file.path(out_tables, "r_alignment_drift_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, strategic_coherence_score), y = strategic_coherence_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Coherence Scores",
      x = "Context",
      y = "Strategic Coherence"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_strategic_coherence_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(contexts, aes(x = alignment_drift_risk, y = strategic_coherence_score, size = governance_strength, label = context_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Alignment Drift Risk and Strategic Coherence",
      x = "Alignment Drift Risk",
      y = "Strategic Coherence",
      size = "Governance Strength"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_drift_coherence_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_strategic_coherence_scores_base.png"), width = 1100, height = 800)
  barplot(
    contexts$strategic_coherence_score,
    names.arg = contexts$context_id,
    main = "Strategic Coherence Scores",
    ylab = "Coherence Score"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "strategic_coherence_score", "alignment_drift_risk")])
