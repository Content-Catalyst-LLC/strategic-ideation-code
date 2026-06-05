# Advanced R workflow for strategic effectiveness profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/strategic_effectiveness_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read.csv(file.path(raw_dir, "strategies.csv"))

strategies$strategic_effectiveness_score <-
  0.18 * strategies$performance +
  0.14 * strategies$alignment +
  0.15 * strategies$resilience +
  0.15 * strategies$adaptability +
  0.13 * strategies$impact +
  0.10 * strategies$learning_value +
  0.06 * strategies$evidence_confidence +
  0.06 * strategies$ethical_resilience -
  0.05 * strategies$measurement_burden +
  0.08 * strategies$strategic_fit

strategies$confidence_adjusted_effectiveness <- strategies$strategic_effectiveness_score * strategies$evidence_confidence

write.csv(
  strategies[order(-strategies$strategic_effectiveness_score), ],
  file.path(out_tables, "r_strategic_effectiveness_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(strategies, aes(x = reorder(strategy_name, strategic_effectiveness_score), y = strategic_effectiveness_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Effectiveness Scores",
      x = "Strategy",
      y = "Effectiveness Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_strategic_effectiveness_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(strategies, aes(x = resilience, y = adaptability, size = performance, label = strategy_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Resilience, Adaptability, and Performance",
      x = "Resilience",
      y = "Adaptability",
      size = "Performance"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_resilience_adaptability_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_strategic_effectiveness_scores_base.png"), width = 1100, height = 800)
  barplot(
    strategies$strategic_effectiveness_score,
    names.arg = strategies$strategy_id,
    main = "Strategic Effectiveness Scores",
    ylab = "Effectiveness Score"
  )
  dev.off()
}

print(strategies[, c("strategy_id", "strategy_name", "strategic_effectiveness_score", "confidence_adjusted_effectiveness")])
