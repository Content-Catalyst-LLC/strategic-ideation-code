# Advanced R workflow for content framework profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/content_framework_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

frameworks <- read.csv(file.path(raw_dir, "frameworks.csv"))

frameworks$framework_strength <-
  0.10 * frameworks$structure_quality +
  0.10 * frameworks$conceptual_clarity +
  0.11 * frameworks$evidence_discipline +
  0.10 * frameworks$assumption_visibility +
  0.10 * frameworks$narrative_coherence +
  0.12 * frameworks$decision_relevance +
  0.10 * frameworks$modularity +
  0.10 * frameworks$reuse_readiness +
  0.08 * frameworks$governance_strength +
  0.06 * frameworks$ethical_visibility +
  0.03 * frameworks$ai_governance

frameworks$framework_risk <-
  0.10 * (1 - frameworks$structure_quality) +
  0.11 * (1 - frameworks$conceptual_clarity) +
  0.12 * (1 - frameworks$evidence_discipline) +
  0.11 * (1 - frameworks$assumption_visibility) +
  0.09 * (1 - frameworks$narrative_coherence) +
  0.12 * (1 - frameworks$decision_relevance) +
  0.09 * (1 - frameworks$modularity) +
  0.09 * (1 - frameworks$reuse_readiness) +
  0.08 * (1 - frameworks$governance_strength) +
  0.06 * (1 - frameworks$ethical_visibility) +
  0.03 * (1 - frameworks$ai_governance)

write.csv(
  frameworks[order(-frameworks$framework_strength), ],
  file.path(out_tables, "r_content_framework_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(frameworks, aes(x = reorder(framework_name, framework_strength), y = framework_strength)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Content Framework Strength",
      x = "Framework",
      y = "Framework Strength"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_framework_strength.png"), width = 11, height = 8, dpi = 160)

  ggplot(frameworks, aes(x = framework_risk, y = framework_strength, size = reuse_readiness, label = framework_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Framework Risk and Reuse Readiness",
      x = "Framework Risk",
      y = "Framework Strength",
      size = "Reuse Readiness"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_framework_risk_reuse_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_framework_strength_base.png"), width = 1100, height = 800)
  barplot(
    frameworks$framework_strength,
    names.arg = frameworks$framework_id,
    main = "Strategic Content Framework Strength",
    ylab = "Framework Strength"
  )
  dev.off()
}

print(frameworks[, c("framework_id", "framework_name", "framework_strength", "framework_risk")])
