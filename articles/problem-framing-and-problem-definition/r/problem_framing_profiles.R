# Advanced R workflow for problem framing and problem definition.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

frames <- read.csv(file.path(raw_dir, "problem_frames.csv"))

frames$problem_framing_score <-
  0.16 * frames$boundary_breadth +
  0.15 * frames$stakeholder_inclusion +
  0.15 * frames$systems_awareness +
  0.16 * frames$causal_depth +
  0.12 * frames$assumption_clarity +
  0.13 * frames$reframing_capacity +
  0.11 * frames$actionability -
  0.10 * frames$institutional_lock_in_risk -
  0.08 * frames$political_convenience_risk

frames$symptom_framing_risk <-
  (1 - frames$causal_depth) * 0.30 +
  (1 - frames$systems_awareness) * 0.25 +
  pmax(0, 0.70 - frames$boundary_breadth) * 0.20 +
  frames$institutional_lock_in_risk * 0.15 +
  frames$political_convenience_risk * 0.10

frames$diagnosis <- ifelse(
  frames$problem_framing_score >= 0.68,
  "strong_problem_framing_capacity",
  ifelse(
    frames$symptom_framing_risk >= 0.62,
    "symptom_or_convenience_frame_risk",
    ifelse(frames$boundary_breadth < 0.45, "boundary_myopia_risk", "develop_with_frame_comparison")
  )
)

write.csv(
  frames[order(-frames$problem_framing_score), ],
  file.path(out_tables, "r_problem_framing_profiles.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(frames, aes(x = reorder(frame_name, problem_framing_score), y = problem_framing_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Problem-Framing Profile Scores",
      x = "Frame",
      y = "Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_problem_framing_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_problem_framing_scores_base.png"), width = 1100, height = 800)
  barplot(
    frames$problem_framing_score,
    names.arg = frames$frame_id,
    main = "Problem-Framing Profile Scores",
    ylab = "Score"
  )
  dev.off()
}

print(frames[, c("frame_id", "frame_name", "problem_framing_score", "symptom_framing_risk", "diagnosis")])
