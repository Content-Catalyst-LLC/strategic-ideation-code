# Advanced R workflow for second-order effects and unintended consequences.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

interventions <- read.csv(file.path(raw_dir, "interventions.csv"))

interventions$second_order_profile_score <-
  0.14 * interventions$first_order_gain -
  0.13 * interventions$adaptation_pressure -
  0.13 * interventions$feedback_amplification -
  0.11 * interventions$delay_risk -
  0.12 * interventions$burden_shift_risk -
  0.12 * interventions$gaming_risk -
  0.15 * interventions$long_term_fragility +
  0.14 * interventions$learning_capacity +
  0.08 * interventions$stakeholder_legitimacy +
  0.08 * interventions$strategic_reversibility

interventions$second_order_risk_score <-
  0.16 * interventions$adaptation_pressure +
  0.15 * interventions$feedback_amplification +
  0.14 * interventions$delay_risk +
  0.15 * interventions$burden_shift_risk +
  0.14 * interventions$gaming_risk +
  0.16 * interventions$long_term_fragility -
  0.10 * interventions$learning_capacity -
  0.06 * interventions$stakeholder_legitimacy -
  0.06 * interventions$strategic_reversibility

interventions$diagnosis <- ifelse(
  interventions$second_order_profile_score >= 0.14,
  "strategically_resilient_profile",
  ifelse(
    interventions$second_order_risk_score >= 0.55,
    "high_second_order_risk",
    "requires_second_order_review"
  )
)

write.csv(
  interventions[order(-interventions$second_order_risk_score), ],
  file.path(out_tables, "r_second_order_effect_profiles.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(interventions, aes(x = reorder(intervention_name, second_order_risk_score), y = second_order_risk_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Second-Order Risk Scores",
      x = "Intervention",
      y = "Risk score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_second_order_risk_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_second_order_risk_scores_base.png"), width = 1100, height = 800)
  barplot(
    interventions$second_order_risk_score,
    names.arg = interventions$intervention_id,
    main = "Second-Order Risk Scores",
    ylab = "Risk"
  )
  dev.off()
}

print(interventions[, c("intervention_id", "intervention_name", "second_order_profile_score", "second_order_risk_score", "diagnosis")])
