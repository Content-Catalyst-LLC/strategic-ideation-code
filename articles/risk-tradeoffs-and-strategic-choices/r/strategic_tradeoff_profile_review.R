# Advanced R workflow for risk, tradeoffs, and strategic choices profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/strategic_tradeoff_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

options <- read.csv(file.path(raw_dir, "strategic_options.csv"))

options$strategic_tradeoff_score <-
  0.18 * options$short_term_return +
  0.20 * options$resilience +
  0.16 * options$flexibility +
  0.14 * options$stakeholder_legitimacy +
  0.14 * options$opportunity_value -
  0.18 * options$exposure +
  0.08 * options$reversibility +
  0.06 * options$implementation_readiness +
  0.08 * options$ethical_resilience +
  0.08 * options$learning_value

options$fragility_warning <-
  0.26 * options$exposure +
  0.18 * (1 - options$resilience) +
  0.14 * (1 - options$flexibility) +
  0.12 * (1 - options$stakeholder_legitimacy) +
  0.12 * (1 - options$opportunity_value) +
  0.10 * (1 - options$reversibility) +
  0.08 * (1 - options$ethical_resilience)

write.csv(
  options[order(-options$strategic_tradeoff_score), ],
  file.path(out_tables, "r_strategic_tradeoff_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(options, aes(x = reorder(option_name, strategic_tradeoff_score), y = strategic_tradeoff_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Tradeoff Profile",
      x = "Option",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_strategic_tradeoff_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(options, aes(x = reorder(option_name, fragility_warning), y = fragility_warning)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Fragility Warning",
      x = "Option",
      y = "Warning"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_strategic_fragility_warning.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_strategic_tradeoff_scores_base.png"), width = 1100, height = 800)
  barplot(
    options$strategic_tradeoff_score,
    names.arg = options$option_id,
    main = "Strategic Tradeoff Profile",
    ylab = "Profile score"
  )
  dev.off()
}

print(options[, c("option_id", "option_name", "strategic_tradeoff_score", "fragility_warning")])
