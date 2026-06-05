# Advanced R workflow for strategic foresight and long-term thinking profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/strategic_foresight_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

profiles <- read.csv(file.path(raw_dir, "foresight_profiles.csv"))

profiles$future_viability_score <-
  0.18 * profiles$foresight_depth +
  0.18 * profiles$resilience +
  0.16 * profiles$flexibility +
  0.14 * profiles$option_value +
  0.12 * profiles$scenario_capacity +
  0.10 * profiles$signal_capacity +
  0.08 * profiles$governance_capacity +
  0.08 * profiles$ethics_review -
  0.14 * profiles$path_dependence_risk

profiles$short_term_bias <-
  profiles$short_term_return -
  rowMeans(profiles[, c("foresight_depth", "resilience", "flexibility", "option_value")])

profiles$foresight_profile_score <-
  0.08 * profiles$short_term_return +
  0.15 * profiles$foresight_depth +
  0.14 * profiles$resilience +
  0.12 * profiles$flexibility -
  0.12 * profiles$path_dependence_risk +
  0.10 * profiles$signal_capacity +
  0.10 * profiles$scenario_capacity +
  0.10 * profiles$option_value +
  0.07 * profiles$ethics_review +
  0.08 * profiles$governance_capacity +
  0.08 * profiles$learning_memory

write.csv(
  profiles[order(-profiles$future_viability_score), ],
  file.path(out_tables, "r_strategic_foresight_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(profiles, aes(x = reorder(strategy_name, future_viability_score), y = future_viability_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Future Viability Score",
      x = "Strategy",
      y = "Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_future_viability_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(profiles, aes(x = reorder(strategy_name, short_term_bias), y = short_term_bias)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Short-Term Optimization Bias",
      x = "Strategy",
      y = "Bias"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_short_term_bias.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_future_viability_scores_base.png"), width = 1100, height = 800)
  barplot(
    profiles$future_viability_score,
    names.arg = profiles$profile_id,
    main = "Future Viability Scores",
    ylab = "Score"
  )
  dev.off()
}

print(profiles[, c("profile_id", "strategy_name", "future_viability_score", "short_term_bias", "foresight_profile_score")])
