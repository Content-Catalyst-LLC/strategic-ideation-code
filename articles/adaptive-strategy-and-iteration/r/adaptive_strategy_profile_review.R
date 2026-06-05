# Advanced R workflow for adaptive strategy and iteration profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/adaptive_strategy_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read.csv(file.path(raw_dir, "strategy_profiles.csv"))

strategies$adaptive_strategy_score <-
  0.13 * strategies$flexibility +
  0.15 * strategies$learning_capacity +
  0.09 * strategies$exploration +
  0.11 * strategies$exploitation_balance +
  0.15 * strategies$coherence +
  0.13 * strategies$feedback_intelligence +
  0.10 * strategies$governance +
  0.08 * strategies$systems_awareness +
  0.06 * strategies$learning_memory

strategies$over_adaptation_risk <-
  0.20 * strategies$flexibility * (1 - strategies$coherence) +
  0.18 * (1 - strategies$governance) +
  0.16 * (1 - strategies$feedback_intelligence) +
  0.14 * (1 - strategies$learning_capacity) +
  0.12 * (1 - strategies$exploitation_balance) +
  0.10 * (1 - strategies$learning_memory) +
  0.10 * (1 - strategies$systems_awareness)

strategies$diagnosis <- ifelse(
  strategies$adaptive_strategy_score >= 0.74,
  "strong_adaptive_strategy_system",
  ifelse(
    strategies$over_adaptation_risk >= 0.60,
    "high_over_adaptation_or_reactivity_risk",
    ifelse(strategies$coherence < 0.45, "strategic_drift_risk", "developing_adaptive_capability")
  )
)

write.csv(
  strategies[order(-strategies$adaptive_strategy_score), ],
  file.path(out_tables, "r_adaptive_strategy_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(strategies, aes(x = reorder(strategy_name, adaptive_strategy_score), y = adaptive_strategy_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Adaptive Strategy Score",
      x = "Strategy",
      y = "Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_adaptive_strategy_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(strategies, aes(x = reorder(strategy_name, over_adaptation_risk), y = over_adaptation_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Over-Adaptation Risk",
      x = "Strategy",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_over_adaptation_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_adaptive_strategy_scores_base.png"), width = 1100, height = 800)
  barplot(
    strategies$adaptive_strategy_score,
    names.arg = strategies$strategy_id,
    main = "Adaptive Strategy Scores",
    ylab = "Score"
  )
  dev.off()
}

print(strategies[, c("strategy_id", "strategy_name", "adaptive_strategy_score", "over_adaptation_risk", "diagnosis")])
