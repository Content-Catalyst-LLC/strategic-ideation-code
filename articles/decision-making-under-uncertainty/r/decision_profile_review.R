# Advanced R workflow for decision-making under uncertainty profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/decision_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

options <- read.csv(file.path(raw_dir, "decision_options.csv"))

options$decision_profile_score <-
  0.14 * options$expected_return +
  0.18 * options$robustness +
  0.16 * options$flexibility +
  0.12 * options$information_quality -
  0.16 * options$exposure +
  0.14 * options$option_value +
  0.10 * options$reversibility +
  0.08 * options$implementation_readiness +
  0.10 * options$ethical_resilience +
  0.10 * options$learning_value

options$fragility_risk <-
  0.24 * options$exposure +
  0.18 * (1 - options$robustness) +
  0.14 * (1 - options$flexibility) +
  0.13 * (1 - options$option_value) +
  0.12 * (1 - options$reversibility) +
  0.10 * (1 - options$ethical_resilience) +
  0.09 * (1 - options$information_quality)

write.csv(
  options[order(-options$decision_profile_score), ],
  file.path(out_tables, "r_decision_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(options, aes(x = reorder(option_name, decision_profile_score), y = decision_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Decision Profile Under Uncertainty",
      x = "Option",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_decision_profile_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(options, aes(x = reorder(option_name, fragility_risk), y = fragility_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Decision Fragility Risk",
      x = "Option",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_decision_fragility_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_decision_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    options$decision_profile_score,
    names.arg = options$option_id,
    main = "Decision Profile Under Uncertainty",
    ylab = "Profile score"
  )
  dev.off()
}

print(options[, c("option_id", "option_name", "decision_profile_score", "fragility_risk")])
