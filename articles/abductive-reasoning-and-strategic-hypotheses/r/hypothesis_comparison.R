# Advanced R workflow for abductive reasoning and strategic hypotheses.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

hypotheses <- read.csv(file.path(raw_dir, "hypotheses.csv"))
evidence <- read.csv(file.path(raw_dir, "evidence_pathways.csv"))

hypotheses$hypothesis_value_score <-
  0.16 * hypotheses$explanatory_strength +
  0.14 * hypotheses$testability +
  0.14 * hypotheses$evidence_quality +
  0.16 * hypotheses$strategic_relevance +
  0.12 * hypotheses$stakeholder_visibility +
  0.12 * hypotheses$systems_fit +
  0.10 * hypotheses$actionability +
  0.06 * hypotheses$reversibility -
  0.10 * hypotheses$implementation_risk

hypotheses$recommended_status <- ifelse(
  hypotheses$hypothesis_value_score >= 0.72 & hypotheses$evidence_quality >= 0.65,
  "prototype_or_pilot",
  ifelse(
    hypotheses$hypothesis_value_score >= 0.64,
    "targeted_research_or_low_risk_test",
    ifelse(hypotheses$hypothesis_value_score >= 0.54, "monitor_and_compare", "hold_reframe_or_archive")
  )
)

evidence$evidence_value_score <-
  0.18 * evidence$evidence_strength +
  0.16 * evidence$reliability +
  0.18 * evidence$discrimination_power +
  0.14 * evidence$stakeholder_legitimacy -
  0.10 * evidence$cost -
  0.08 * evidence$time_to_learn

write.csv(hypotheses[order(-hypotheses$hypothesis_value_score), ], file.path(out_tables, "r_hypothesis_scores.csv"), row.names = FALSE)
write.csv(evidence[order(-evidence$evidence_value_score), ], file.path(out_tables, "r_evidence_scores.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(hypotheses, aes(x = reorder(hypothesis_name, hypothesis_value_score), y = hypothesis_value_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Hypothesis Value Scores",
      x = "Hypothesis",
      y = "Value score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_hypothesis_value_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_hypothesis_value_scores_base.png"), width = 1100, height = 800)
  barplot(
    hypotheses$hypothesis_value_score,
    names.arg = hypotheses$hypothesis_id,
    main = "Strategic Hypothesis Value Scores",
    ylab = "Value score"
  )
  dev.off()
}

print(hypotheses[, c("hypothesis_id", "hypothesis_name", "hypothesis_value_score", "recommended_status")])
