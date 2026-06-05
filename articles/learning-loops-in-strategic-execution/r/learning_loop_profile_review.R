# Advanced R workflow for learning loop profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/learning_loop_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "learning_contexts.csv"))

contexts$learning_loop_strength <-
  0.12 * contexts$feedback_quality +
  0.12 * contexts$assumption_review +
  0.11 * contexts$interpretation_discipline +
  0.13 * contexts$decision_authority +
  0.13 * contexts$learning_closure +
  0.10 * contexts$decision_memory +
  0.08 * contexts$psychological_safety +
  0.08 * contexts$knowledge_scaling +
  0.08 * contexts$ethical_learning +
  0.07 * contexts$strategic_coherence +
  0.08 * contexts$adaptive_capacity

contexts$learning_failure_risk <-
  0.11 * (1 - contexts$feedback_quality) +
  0.12 * (1 - contexts$assumption_review) +
  0.10 * (1 - contexts$interpretation_discipline) +
  0.14 * (1 - contexts$decision_authority) +
  0.14 * (1 - contexts$learning_closure) +
  0.11 * (1 - contexts$decision_memory) +
  0.08 * (1 - contexts$psychological_safety) +
  0.08 * (1 - contexts$knowledge_scaling) +
  0.08 * (1 - contexts$ethical_learning) +
  0.07 * (1 - contexts$strategic_coherence) +
  0.07 * (1 - contexts$adaptive_capacity)

write.csv(
  contexts[order(-contexts$learning_loop_strength), ],
  file.path(out_tables, "r_learning_loop_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, learning_loop_strength), y = learning_loop_strength)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Learning Loop Strength",
      x = "Context",
      y = "Learning Loop Strength"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_learning_loop_strength.png"), width = 11, height = 8, dpi = 160)

  ggplot(contexts, aes(x = learning_failure_risk, y = learning_loop_strength, size = decision_authority, label = context_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Learning Failure Risk and Learning Loop Strength",
      x = "Learning Failure Risk",
      y = "Learning Loop Strength",
      size = "Decision Authority"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_learning_risk_strength_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_learning_loop_strength_base.png"), width = 1100, height = 800)
  barplot(
    contexts$learning_loop_strength,
    names.arg = contexts$context_id,
    main = "Strategic Learning Loop Strength",
    ylab = "Loop Strength"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "learning_loop_strength", "learning_failure_risk")])
