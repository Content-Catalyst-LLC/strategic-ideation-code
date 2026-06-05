# Advanced R workflow for strategic idea portfolio review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/strategic_portfolio_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(raw_dir, "strategic_ideas.csv"))

ideas$portfolio_contribution <-
  0.17 * ideas$impact +
  0.16 * ideas$strategic_fit +
  0.15 * ideas$learning_value +
  0.15 * ideas$option_value +
  0.12 * ideas$ethical_resilience +
  0.10 * ideas$evidence_strength +
  0.08 * ideas$governance_readiness -
  0.10 * ideas$risk -
  0.08 * ideas$capacity_demand -
  0.04 * pmin(ideas$dependency_count / 6, 1)

ideas$overload_warning <-
  0.30 * ideas$capacity_demand +
  0.24 * ideas$risk +
  0.14 * (1 - ideas$strategic_fit) +
  0.12 * (1 - ideas$ethical_resilience) +
  0.10 * (1 - ideas$option_value) +
  0.10 * pmin(ideas$dependency_count / 6, 1)

write.csv(
  ideas[order(-ideas$portfolio_contribution), ],
  file.path(out_tables, "r_strategic_portfolio_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(ideas, aes(x = reorder(idea_name, portfolio_contribution), y = portfolio_contribution)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Idea Portfolio Contribution",
      x = "Idea",
      y = "Contribution"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_portfolio_contribution_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(ideas, aes(x = reorder(idea_name, overload_warning), y = overload_warning)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Portfolio Overload Warning",
      x = "Idea",
      y = "Warning"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_portfolio_overload_warning.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_portfolio_contribution_scores_base.png"), width = 1100, height = 800)
  barplot(
    ideas$portfolio_contribution,
    names.arg = ideas$idea_id,
    main = "Strategic Idea Portfolio Contribution",
    ylab = "Contribution"
  )
  dev.off()
}

print(ideas[, c("idea_id", "idea_name", "role", "portfolio_contribution", "overload_warning")])
