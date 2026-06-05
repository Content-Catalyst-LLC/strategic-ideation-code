# Advanced R workflow for feedback-loop design profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/feedback_loop_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read.csv(file.path(raw_dir, "feedback_systems.csv"))

systems$feedback_profile_score <-
  0.13 * systems$signal_quality +
  0.13 * systems$interpretation_capacity +
  0.10 * systems$adjustment_speed +
  0.13 * systems$user_insight_depth +
  0.10 * systems$stability +
  0.11 * systems$ethical_integrity +
  0.10 * systems$systems_awareness +
  0.10 * systems$decision_linkage +
  0.10 * systems$learning_memory

systems$noisy_churn_risk <-
  0.16 * systems$adjustment_speed +
  0.15 * (1 - systems$signal_quality) +
  0.15 * (1 - systems$interpretation_capacity) +
  0.13 * (1 - systems$stability) +
  0.12 * (1 - systems$systems_awareness) +
  0.12 * (1 - systems$ethical_integrity) +
  0.10 * (1 - systems$decision_linkage) +
  0.07 * (1 - systems$learning_memory)

systems$diagnosis <- ifelse(
  systems$feedback_profile_score >= 0.68,
  "strong_feedback_learning_system",
  ifelse(
    systems$noisy_churn_risk >= 0.64,
    "high_noisy_churn_or_feedback_theater_risk",
    ifelse(systems$decision_linkage < 0.40, "feedback_not_linked_to_decisions", "developing_feedback_capability")
  )
)

write.csv(
  systems[order(-systems$feedback_profile_score), ],
  file.path(out_tables, "r_feedback_loop_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(systems, aes(x = reorder(system_name, feedback_profile_score), y = feedback_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Feedback-Loop Design Profile",
      x = "System",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_feedback_profile_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(systems, aes(x = reorder(system_name, noisy_churn_risk), y = noisy_churn_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Noisy Churn Risk in Feedback Systems",
      x = "System",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_noisy_churn_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_feedback_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    systems$feedback_profile_score,
    names.arg = systems$system_id,
    main = "Feedback Profile Scores",
    ylab = "Score"
  )
  dev.off()
}

print(systems[, c("system_id", "system_name", "feedback_profile_score", "noisy_churn_risk", "diagnosis")])
