# Advanced R workflow for strategic ideation portfolio comparison.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(raw_dir, "idea_portfolio.csv"))
assumptions <- read.csv(file.path(raw_dir, "assumptions.csv"))
options <- read.csv(file.path(raw_dir, "option_architecture.csv"))

assumptions$assumption_risk <- (1 - assumptions$confidence) * assumptions$criticality
assumption_risk <- aggregate(assumption_risk ~ idea_id, data = assumptions, FUN = mean)

portfolio <- merge(ideas, assumption_risk, by = "idea_id", all.x = TRUE)
portfolio$assumption_risk[is.na(portfolio$assumption_risk)] <- 0

portfolio$portfolio_score <-
  0.20 * portfolio$strategic_fit +
  0.12 * portfolio$feasibility +
  0.18 * portfolio$systems_leverage +
  0.13 * portfolio$learning_value +
  0.16 * portfolio$ethical_legitimacy +
  0.09 * portfolio$knowledge_reusability -
  0.07 * portfolio$uncertainty -
  0.05 * portfolio$assumption_risk

portfolio$revision_flag <- ifelse(
  portfolio$assumption_risk > 0.40 | portfolio$uncertainty > 0.38,
  "test_before_commitment",
  ifelse(portfolio$portfolio_score > 0.80, "advance_to_strategy_review", "prototype_or_reframe")
)

options$architecture_score <-
  0.16 * options$reversibility -
  0.10 * options$dependency_complexity +
  0.24 * options$portfolio_fit +
  0.24 * options$scenario_robustness +
  0.22 * options$sequencing_value

write.csv(portfolio[order(-portfolio$portfolio_score), ], file.path(out_tables, "r_idea_portfolio_scores.csv"), row.names = FALSE)
write.csv(assumptions[order(-assumptions$assumption_risk), ], file.path(out_tables, "r_assumption_risk_register.csv"), row.names = FALSE)
write.csv(options[order(-options$architecture_score), ], file.path(out_tables, "r_option_architecture_scores.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(portfolio, aes(x = reorder(idea_name, portfolio_score), y = portfolio_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Ideation Portfolio Scores",
      x = "Idea",
      y = "Portfolio score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_idea_portfolio_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_idea_portfolio_scores_base.png"), width = 1100, height = 800)
  barplot(
    portfolio$portfolio_score,
    names.arg = portfolio$idea_id,
    main = "Strategic Ideation Portfolio Scores",
    ylab = "Portfolio score"
  )
  dev.off()
}

print(portfolio[, c("idea_id", "idea_name", "portfolio_score", "assumption_risk", "revision_flag")])
