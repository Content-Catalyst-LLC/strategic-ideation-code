# Advanced R workflow for assumption mapping.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/assumption_risk_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

assumptions <- read.csv(file.path(raw_dir, "assumptions.csv"))

assumptions$evidence_composite <-
  0.40 * assumptions$evidence_strength +
  0.30 * assumptions$evidence_relevance +
  0.30 * assumptions$evidence_transferability

assumptions$priority_score <- assumptions$criticality * assumptions$uncertainty

assumptions$evidence_adjusted_risk <-
  assumptions$criticality *
  assumptions$uncertainty *
  (1 - assumptions$evidence_composite)

assumptions$learning_value <-
  0.34 * assumptions$evidence_adjusted_risk +
  0.24 * assumptions$testability +
  0.18 * assumptions$stakeholder_sensitivity +
  0.14 * assumptions$system_sensitivity +
  0.10 * assumptions$criticality

assumptions$diagnosis <- ifelse(
  assumptions$evidence_adjusted_risk >= 0.28 & assumptions$testability >= 0.65,
  "test_first",
  ifelse(
    assumptions$evidence_adjusted_risk >= 0.28,
    "reduce_commitment_before_testing",
    ifelse(
      assumptions$stakeholder_sensitivity >= 0.85,
      "stakeholder_review_required",
      "monitor"
    )
  )
)

write.csv(
  assumptions[order(-assumptions$evidence_adjusted_risk), ],
  file.path(out_tables, "r_assumption_risk_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(assumptions, aes(x = uncertainty, y = criticality, label = assumption_id)) +
    geom_point(size = 3) +
    geom_text(nudge_y = 0.02, check_overlap = TRUE) +
    labs(
      title = "Assumption Criticality and Uncertainty",
      x = "Uncertainty",
      y = "Criticality"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_assumption_criticality_uncertainty.png"), width = 10, height = 7, dpi = 160)

  ggplot(assumptions, aes(x = reorder(assumption_id, evidence_adjusted_risk), y = evidence_adjusted_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Evidence-Adjusted Assumption Risk",
      x = "Assumption",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_assumption_risk_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_assumption_risk_scores_base.png"), width = 1100, height = 800)
  barplot(
    assumptions$evidence_adjusted_risk,
    names.arg = assumptions$assumption_id,
    main = "Evidence-Adjusted Assumption Risk",
    ylab = "Risk"
  )
  dev.off()
}

print(assumptions[, c("assumption_id", "assumption_type", "evidence_adjusted_risk", "learning_value", "diagnosis")])
