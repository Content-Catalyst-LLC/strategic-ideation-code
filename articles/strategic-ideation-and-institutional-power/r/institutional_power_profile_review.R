# Advanced R workflow for institutional power profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/institutional_power_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(raw_dir, "power_ideas.csv"))

ideas$merit_score <-
  0.28 * ideas$strategic_merit +
  0.21 * ideas$evidence_strength +
  0.16 * ideas$stakeholder_influence +
  0.13 * ideas$dissent_protection +
  0.12 * ideas$classification_visibility +
  0.10 * ideas$ethical_visibility

ideas$institutional_support <-
  0.28 * ideas$executive_sponsorship +
  0.24 * ideas$resource_fit +
  0.24 * ideas$power_alignment +
  0.24 * ideas$advancement_likelihood

ideas$power_distortion <- ideas$institutional_support - ideas$merit_score
ideas$voice_gap <- ideas$advancement_likelihood - ideas$stakeholder_influence

write.csv(
  ideas[order(-ideas$power_distortion), ],
  file.path(out_tables, "r_institutional_power_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(ideas, aes(x = reorder(idea, power_distortion), y = power_distortion)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Power Distortion in Strategic Idea Advancement",
      x = "Idea",
      y = "Institutional Support Minus Merit"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_power_distortion.png"), width = 11, height = 8, dpi = 160)

  ggplot(ideas, aes(x = merit_score, y = institutional_support, size = power_alignment, label = idea_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Strategic Merit and Institutional Support",
      x = "Merit Score",
      y = "Institutional Support",
      size = "Power Alignment"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_merit_institutional_support.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_power_distortion_base.png"), width = 1100, height = 800)
  barplot(
    ideas$power_distortion,
    names.arg = ideas$idea_id,
    main = "Power Distortion in Strategic Idea Advancement",
    ylab = "Institutional Support Minus Merit"
  )
  dev.off()
}

print(ideas[, c("idea_id", "idea", "merit_score", "institutional_support", "power_distortion", "voice_gap")])
