# Strategic ideation portfolio comparison workflow
# Uses base R only so it can run without package installation.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
data_dir <- file.path(root, "data", "raw")
out_dir <- file.path(root, "outputs", "tables")
fig_dir <- file.path(root, "outputs", "figures")
processed_dir <- file.path(root, "data", "processed")

dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(processed_dir, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(data_dir, "synthetic_ideas.csv"))
criteria <- read.csv(file.path(data_dir, "criteria.csv"))
assumptions <- read.csv(file.path(data_dir, "assumptions.csv"))

weights <- setNames(criteria$weight, criteria$criterion)

assumption_risk <- aggregate(
  (1 - confidence) * criticality ~ idea_id,
  data = assumptions,
  FUN = mean
)

names(assumption_risk)[2] <- "assumption_risk"

portfolio <- merge(ideas, assumption_risk, by = "idea_id", all.x = TRUE)
portfolio$assumption_risk[is.na(portfolio$assumption_risk)] <- 0

portfolio$portfolio_score <-
  weights["strategic_fit"] * portfolio$strategic_fit +
  weights["feasibility"] * portfolio$feasibility +
  weights["systems_leverage"] * portfolio$systems_leverage +
  weights["learning_value"] * portfolio$learning_value +
  weights["ethical_legitimacy"] * portfolio$ethical_legitimacy -
  weights["uncertainty_penalty"] * portfolio$uncertainty -
  0.12 * portfolio$assumption_risk

portfolio$revision_flag <- ifelse(
  portfolio$assumption_risk > 0.35 | portfolio$uncertainty > 0.35,
  "needs_revision",
  "ready_for_review"
)

portfolio <- portfolio[order(-portfolio$portfolio_score), ]

write.csv(
  portfolio,
  file.path(out_dir, "r_portfolio_comparison.csv"),
  row.names = FALSE
)

write.csv(
  portfolio,
  file.path(processed_dir, "r_portfolio_comparison.csv"),
  row.names = FALSE
)

png(file.path(fig_dir, "r_portfolio_scores.png"), width = 1000, height = 700)
barplot(
  portfolio$portfolio_score,
  names.arg = portfolio$idea_id,
  las = 2,
  main = "Strategic Ideation Portfolio Scores",
  ylab = "Score"
)
dev.off()

print(portfolio[, c("idea_id", "idea_name", "portfolio_score", "assumption_risk", "revision_flag")])
