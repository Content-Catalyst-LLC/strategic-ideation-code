# Advanced R workflow for idea-to-strategy profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/idea_to_strategy_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

initiatives <- read.csv(file.path(raw_dir, "initiatives.csv"))

initiatives$strategy_conversion_score <-
  0.14 * initiatives$feasibility +
  0.15 * initiatives$viability +
  0.13 * initiatives$desirability -
  0.11 * initiatives$integration_difficulty +
  0.15 * initiatives$execution_readiness +
  0.13 * initiatives$strategic_fit +
  0.08 * initiatives$evidence_confidence +
  0.08 * initiatives$ethical_resilience -
  0.07 * initiatives$resource_intensity +
  0.10 * initiatives$governance_readiness +
  0.06 * initiatives$learning_value

initiatives$confidence_adjusted_score <- initiatives$strategy_conversion_score * initiatives$evidence_confidence

write.csv(
  initiatives[order(-initiatives$strategy_conversion_score), ],
  file.path(out_tables, "r_idea_to_strategy_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(initiatives, aes(x = reorder(initiative_name, strategy_conversion_score), y = strategy_conversion_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Idea-to-Strategy Conversion Scores",
      x = "Initiative",
      y = "Conversion Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_strategy_conversion_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(initiatives, aes(x = integration_difficulty, y = execution_readiness, size = strategic_fit, label = initiative_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Integration Difficulty and Execution Readiness",
      x = "Integration Difficulty",
      y = "Execution Readiness",
      size = "Strategic Fit"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_integration_execution_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_strategy_conversion_scores_base.png"), width = 1100, height = 800)
  barplot(
    initiatives$strategy_conversion_score,
    names.arg = initiatives$initiative_id,
    main = "Idea-to-Strategy Conversion Scores",
    ylab = "Conversion Score"
  )
  dev.off()
}

print(initiatives[, c("initiative_id", "initiative_name", "strategy_conversion_score", "confidence_adjusted_score")])
