# Advanced R workflow for boundary setting in strategic ideation.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

boundaries <- read.csv(file.path(raw_dir, "boundary_frames.csv"))

boundaries$boundary_quality_score <-
  0.12 * boundaries$problem_clarity +
  0.13 * boundaries$system_context +
  0.14 * boundaries$stakeholder_inclusion +
  0.14 * boundaries$causal_adequacy +
  0.12 * boundaries$temporal_adequacy +
  0.11 * boundaries$institutional_responsibility +
  0.11 * boundaries$evidence_diversity +
  0.10 * boundaries$ethical_review +
  0.09 * boundaries$revision_readiness +
  0.04 * boundaries$actionability

boundaries$diagnosis <- ifelse(
  boundaries$boundary_quality_score >= 0.78,
  "strong_boundary_design",
  ifelse(
    boundaries$stakeholder_inclusion < 0.40,
    "stakeholder_exclusion_risk",
    ifelse(
      boundaries$temporal_adequacy < 0.40,
      "temporal_boundary_risk",
      ifelse(
        boundaries$causal_adequacy < 0.45,
        "causal_boundary_risk",
        "usable_with_boundary_review"
      )
    )
  )
)

write.csv(
  boundaries[order(-boundaries$boundary_quality_score), ],
  file.path(out_tables, "r_boundary_profile_scores.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(boundaries, aes(x = reorder(boundary_name, boundary_quality_score), y = boundary_quality_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Boundary Quality Scores",
      x = "Boundary Frame",
      y = "Boundary Quality"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_boundary_quality_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_boundary_quality_scores_base.png"), width = 1100, height = 800)
  barplot(
    boundaries$boundary_quality_score,
    names.arg = boundaries$boundary_id,
    main = "Boundary Quality Scores",
    ylab = "Score"
  )
  dev.off()
}

print(boundaries[, c("boundary_id", "boundary_name", "boundary_quality_score", "diagnosis")])
