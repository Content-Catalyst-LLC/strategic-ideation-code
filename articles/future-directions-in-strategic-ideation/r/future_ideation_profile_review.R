# Advanced R workflow for future-ready strategic ideation profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/future_ideation_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(raw_dir, "future_ideas.csv"))

ideas$future_ready_score <-
  0.10 * ideas$problem_frame_quality +
  0.10 * ideas$evidence_quality +
  0.10 * ideas$adaptability +
  0.11 * ideas$scenario_robustness +
  0.10 * ideas$stakeholder_legitimacy +
  0.09 * ideas$implementation_readiness +
  0.10 * ideas$ethical_visibility +
  0.11 * ideas$learning_design +
  0.08 * ideas$option_value +
  0.06 * ideas$ai_governance +
  0.05 * ideas$systems_responsibility

ideas$future_risk <- 1 - ideas$future_ready_score

write.csv(
  ideas[order(-ideas$future_ready_score), ],
  file.path(out_tables, "r_future_ideation_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(ideas, aes(x = reorder(idea, future_ready_score), y = future_ready_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Future-Ready Strategic Idea Scores",
      x = "Idea",
      y = "Future-Ready Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_future_ready_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(ideas, aes(x = scenario_robustness, y = learning_design, size = option_value, label = idea_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Scenario Robustness, Learning Design, and Option Value",
      x = "Scenario Robustness",
      y = "Learning Design",
      size = "Option Value"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_scenario_learning_option_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_future_ready_scores_base.png"), width = 1100, height = 800)
  barplot(
    ideas$future_ready_score,
    names.arg = ideas$idea_id,
    main = "Future-Ready Strategic Idea Scores",
    ylab = "Future-Ready Score"
  )
  dev.off()
}

print(ideas[, c("idea_id", "idea", "future_ready_score", "future_risk")])
