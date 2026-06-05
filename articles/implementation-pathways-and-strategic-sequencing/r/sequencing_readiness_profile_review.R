# Advanced R workflow for sequencing readiness profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/sequencing_readiness_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

pathways <- read.csv(file.path(raw_dir, "pathways.csv"))

pathways$sequencing_readiness_score <-
  0.15 * pathways$capability_readiness +
  0.14 * pathways$evidence_strength +
  0.14 * pathways$governance_readiness +
  0.13 * pathways$legitimacy -
  0.10 * pathways$dependency_load +
  0.09 * pathways$reversibility -
  0.09 * pathways$capacity_demand +
  0.07 * pathways$timing_urgency +
  0.11 * pathways$ethical_resilience +
  0.09 * pathways$feedback_strength +
  0.10 * pathways$strategic_fit

pathways$premature_commitment_risk <-
  0.22 * pathways$dependency_load +
  0.20 * pathways$capacity_demand +
  0.16 * (1 - pathways$evidence_strength) +
  0.14 * (1 - pathways$governance_readiness) +
  0.12 * (1 - pathways$reversibility) +
  0.10 * (1 - pathways$ethical_resilience) +
  0.06 * (1 - pathways$feedback_strength)

write.csv(
  pathways[order(-pathways$sequencing_readiness_score), ],
  file.path(out_tables, "r_sequencing_readiness_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(pathways, aes(x = reorder(pathway_name, sequencing_readiness_score), y = sequencing_readiness_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Implementation Pathway Sequencing Readiness",
      x = "Pathway",
      y = "Sequencing Readiness"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_pathway_readiness_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(pathways, aes(x = dependency_load, y = capacity_demand, size = timing_urgency, label = pathway_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Dependency Load, Capacity Demand, and Timing Urgency",
      x = "Dependency Load",
      y = "Capacity Demand",
      size = "Timing Urgency"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_dependency_capacity_timing_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_pathway_readiness_scores_base.png"), width = 1100, height = 800)
  barplot(
    pathways$sequencing_readiness_score,
    names.arg = pathways$pathway_id,
    main = "Sequencing Readiness Scores",
    ylab = "Readiness Score"
  )
  dev.off()
}

print(pathways[, c("pathway_id", "pathway_name", "sequencing_readiness_score", "premature_commitment_risk")])
