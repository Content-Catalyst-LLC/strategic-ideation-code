# Advanced R workflow for bad-idea risk profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/bad_idea_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(raw_dir, "bad_ideas.csv"))

ideas$idea_quality <-
  0.12 * ideas$problem_frame_integrity +
  0.11 * ideas$mechanism_clarity +
  0.13 * ideas$evidence_quality +
  0.10 * ideas$context_fit +
  0.12 * ideas$implementation_readiness +
  0.10 * ideas$incentive_alignment +
  0.10 * ideas$ethical_visibility +
  0.09 * ideas$strategic_merit +
  0.08 * ideas$learning_design +
  0.05 * ideas$narrative_honesty

ideas$power_distortion <- ideas$institutional_support - ideas$strategic_merit

positive_power_distortion <- pmax(0, ideas$power_distortion)

ideas$failure_risk <-
  0.12 * (1 - ideas$problem_frame_integrity) +
  0.11 * (1 - ideas$mechanism_clarity) +
  0.13 * (1 - ideas$evidence_quality) +
  0.10 * (1 - ideas$context_fit) +
  0.12 * (1 - ideas$implementation_readiness) +
  0.10 * (1 - ideas$incentive_alignment) +
  0.10 * (1 - ideas$ethical_visibility) +
  0.08 * (1 - ideas$learning_design) +
  0.05 * (1 - ideas$narrative_honesty) +
  0.05 * positive_power_distortion +
  0.04 * ideas$ai_fluency_risk

write.csv(
  ideas[order(-ideas$failure_risk), ],
  file.path(out_tables, "r_bad_idea_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(ideas, aes(x = reorder(idea, failure_risk), y = failure_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Bad-Idea Failure Risk",
      x = "Idea",
      y = "Failure Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_bad_idea_failure_risk.png"), width = 11, height = 8, dpi = 160)

  ggplot(ideas, aes(x = idea_quality, y = failure_risk, size = positive_power_distortion, label = idea_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Idea Quality and Failure Risk",
      x = "Idea Quality",
      y = "Failure Risk",
      size = "Power Distortion"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_idea_quality_failure_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_bad_idea_failure_risk_base.png"), width = 1100, height = 800)
  barplot(
    ideas$failure_risk,
    names.arg = ideas$idea_id,
    main = "Bad-Idea Failure Risk",
    ylab = "Failure Risk"
  )
  dev.off()
}

print(ideas[, c("idea_id", "idea", "idea_quality", "failure_risk", "power_distortion")])
