# Advanced R workflow for imagination, discipline, and strategic creativity.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(raw_dir, "creative_ideas.csv"))

ideas$strategic_creativity_score <-
  0.14 * ideas$novelty +
  0.16 * ideas$strategic_relevance +
  0.13 * ideas$conceptual_coherence +
  0.14 * ideas$mechanism_clarity +
  0.11 * ideas$testability +
  0.13 * ideas$stakeholder_grounding +
  0.13 * ideas$systems_fit +
  0.12 * ideas$developmental_potential +
  0.08 * ideas$revision_capacity -
  0.12 * ideas$implementation_risk

ideas$novelty_theater_risk <- ideas$novelty *
  (1 - ((ideas$mechanism_clarity + ideas$systems_fit + ideas$stakeholder_grounding) / 3))

ideas$diagnosis <- ifelse(
  ideas$novelty_theater_risk >= 0.42,
  "novelty_theater_risk",
  ifelse(
    ideas$stakeholder_grounding < 0.45,
    "stakeholder_grounding_gap",
    ifelse(
      ideas$systems_fit < 0.50,
      "systems_fit_gap",
      ifelse(ideas$strategic_creativity_score >= 0.70, "strong_candidate", "develop_or_reframe")
    )
  )
)

write.csv(
  ideas[order(-ideas$strategic_creativity_score), ],
  file.path(out_tables, "r_strategic_creativity_profiles.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(ideas, aes(x = reorder(idea_name, strategic_creativity_score), y = strategic_creativity_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Creativity Scores",
      x = "Idea",
      y = "Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_strategic_creativity_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_strategic_creativity_scores_base.png"), width = 1100, height = 800)
  barplot(
    ideas$strategic_creativity_score,
    names.arg = ideas$idea_id,
    main = "Strategic Creativity Scores",
    ylab = "Score"
  )
  dev.off()
}

print(ideas[, c("idea_id", "idea_name", "strategic_creativity_score", "novelty_theater_risk", "diagnosis")])
